import sqlite3
from re import fullmatch
from helpers.myFuncs import fetch_as_dict
from werkzeug.security import check_password_hash, generate_password_hash


class Student:
    """
    A class that stores students in a database and allow mutiple function on them.
    """

    db = sqlite3.connect("students.db", check_same_thread=False)
    c = db.cursor()

    def __init__(
        self,
        name: str,
        password: str,
        national_id: str,
        grade: int,
        specialization: str,
    ):
        """
        It Creates a link to the database
        """
        self.name = name
        self.password = password
        self.national_id = national_id
        self.grade = grade
        self.specialization = specialization

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if type(password) is not str:
            raise (TypeError)
        # got this pattern from RockOnGom's comment on stackoverflow https://stackoverflow.com/a/5142164
        pattern = (
            r"(?=.*([A-Z]){1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,100}"
        )
        if fullmatch(pattern, password) is None:
            raise ValueError("الباسورد ضعيف للغاية")
        self._password = password

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, national_id: str):
        # check if it follows the format
        if type(national_id) is not str:
            raise (TypeError)
        if (
            fullmatch(r"(2|3)\d{4}([1-9]|[12][0-9]|3[01])\d{6}[1-9]", national_id)
            is None
        ):
            raise ValueError("الرقم القومي غير صحيح")
        national_ids = Student.c.execute("SELECT national_id FROM students").fetchall()
        for n in national_ids:
            if check_password_hash(n[0],national_id) == True:
                raise ValueError("الطالب مسجل بالفعل")
        self._national_id = national_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if type(name) is not str:
            raise (TypeError)
        # this pattern matches 3 arabic words with a single space inbetween
        pattern = r"(?:[\u0621-\u064A]+ ){2}[\u0621-\u064A]+"
        if fullmatch(pattern, name) is None:
            raise ValueError("اسم الطالب غير صحيح")
        self._name = name

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade: int):
        try:
            grade = int(grade)
        except TypeError:
            raise TypeError("العام الدراسي يجب ان يكون عددا موجبا")
        if grade not in [11, 12]:
            raise ValueError("العام الدراسي يجب ان يكون 11 او 12")
        self._grade = grade

    @property
    def specialization(self):
        return self._specialization

    @specialization.setter
    def specialization(self, specialization: str):
        if specialization not in [
            "scientific",
            "literature",
            "math_oriented",
            "science_oriented",
        ]:
            raise ValueError("التخصص خطأ")
        self._specialization = specialization

    def add(self):
        Student.c.execute(
            """INSERT INTO students  (name,
                                      password,
                                      national_id,
                                      grade,
                                      specialization)
                                      Values(?,?,?,?,?)""",
            [
                self.name,
                generate_password_hash(self.password),
                generate_password_hash(self.national_id),
                self.grade,
                self.specialization,
            ],
        )
        Student.db.commit()
        return "تم اضافة الطالب بنجاح"

    def isexist(name: str, national_id: str, password: str) -> bool:
        users = fetch_as_dict(
            Student.c, "SELECT id,name,password,national_id FROM students"
        )
        for user in users:
            print(user)
            print(user["password"])
            if check_password_hash(user["password"], password) == False:
                continue
            if check_password_hash(user["national_id"], national_id) == False:
                continue
            if not user["name"] == name:
                continue
            return user["id"]
        return False
    
    def delete(data: dict):
        if (id := Student.isexist(**data)) is False:
            return "الطالب لا يوجد في قاعدة البيانات"
        print(type(id))
        Student.c.execute("DELETE FROM students WHERE id = ?",(id, ))
        Student.db.commit()
        return "تم حذف بيانات الطالب بنجاح"
        
