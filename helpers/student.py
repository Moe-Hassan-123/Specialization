import sqlite3
from re import fullmatch
from helpers.myFunctions import fetch_as_dict, translate
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
        Saves The student in the database and returns his ID.
        """
        if (Student.isexist(name, national_id, password)) is not False:
            raise ValueError("الطالب مسجل بالفعل")
        self.name = name
        self.password = password
        self.national_id = national_id
        self.grade = grade
        self.specialization = specialization
        self.id = Student.add(self)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if type(password) is not str:
            return TypeError
        pattern = r"^(?=.*[0-9])(?=.*[a-z]).{8,32}$"
        if fullmatch(pattern, password) is None:
            raise ValueError(".الباسورد يجب ان يكون 8 حروف او اكثر و يحتوي علي رقم")
        self._password = password

    @property
    def national_id(self):
        return self._national_id

    # current best
    #
    #
    # 16 STEP "2|3\d{2}(0[1-9]|1[012])(?:0[1-9]|[12][0-9]|3[01])\d{7}"
    @national_id.setter
    def national_id(self, national_id: str):
        # check if it follows the format
        if type(national_id) is not str:
            raise (TypeError)
        if (
            fullmatch(
                r"(2|3)\d{2}((0[1-9])|(1[012]))((0[1-9])|1[0-9]|2[0-9]|3[01])\d{7}",
                national_id,
            )
            is None
        ):
            raise ValueError("الرقم القومي غير صحيح.")

        # Make sure the National id is unique
        national_ids = Student.c.execute("SELECT national_id FROM students").fetchall()
        for n in national_ids:
            if check_password_hash(n[0], national_id) == True:
                raise ValueError("الرقم القومي مسجل بقاعدة البيانات")
        self._national_id = national_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if type(name) is not str:
            raise (TypeError)

        # Handle All White Space in the name
        # this pattern matches 3 arabic words with a single space inbetween
        pattern = r" *[\u0621-\u064A\u0660-\u0669]+ +[\u0621-\u064A\u0660-\u0669]+ +[\u0621-\u064A\u0660-\u0669]+ *"
        name = " ".join(map(str.strip, name.strip().split()))
        if fullmatch(pattern, name) is None:
            raise ValueError(".اسم الطالب غير صحيح")
        self._name = name

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade: int):
        try:
            grade = int(grade)
        except TypeError:
            raise TypeError(".العام الدراسي خطأ")
        if grade not in [1, 2]:
            raise ValueError("العام الدراسي يجب ان يكون ثانية ثانوي او ثالثة ثانوي")
        self._grade = grade

    @property
    def specialization(self):
        return self._specialization

    @specialization.setter
    def specialization(self, specialization: str):
        if (
            self.grade == 1
            and specialization not in ["s", "l"]
            or self.grade == 2
            and specialization not in ["l", "m", "o"]
        ):
            raise ValueError("التخصص خطأ")
        self._specialization = specialization

    def add(self):
        """
        Adds The student to the Database
        """

        id = Student.c.execute(
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
        ).lastrowid
        if id == None:
            raise Exception("لم يتم تسجيل الطالب")
        Student.db.commit()
        return id

    def isexist(name: str, national_id: str, password: str) -> int | bool:
        """Checks if a student Exists in the Database

        Args:
            name (str): The Name of the student
            national_id (str): The National Id of The Student
            password (str): The Password of The Student

        Returns:
            int: The id of The student if it was in the database else False
        """
        users = fetch_as_dict(
            Student.c, "SELECT id,name,password,national_id FROM students"
        )
        for user in users:
            if check_password_hash(user["password"], password) == False:
                continue
            if check_password_hash(user["national_id"], national_id) == False:
                continue
            if not user["name"] == name:
                continue
            return user["id"]
        return False

    def delete(id) -> str:
        """Deletes A student from the database

        Args:
            data (dict): Students Info

        Returns:
            (string): A message that shows whether the process was a Success or Failure
        """
        Student.c.execute("DELETE FROM students WHERE id = ?", (id,))
        Student.db.commit()
        return "تم حذف بيانات الطالب بنجاح"

    def edit(id: int, new_specialization: str, grade: int) -> str:
        """Changes The Speciality of the Student

        Args:
            data (dict): Students Info
            new_specialization (int): The New Speciality Student Wants

        Returns:
            (string): a Message that shows the status of change
        """
        old = fetch_as_dict(
            Student.c, "SELECT grade, specialization FROM students WHERE id = ?", id
        )[0]

        # Student Changed Nothing
        if old["grade"] == grade and old["specialization"] == new_specialization:
            return f".البيانات متطابقة مع بياناتك الحالية. لم يتم اي تغيير"

        Student.c.execute(
            """
                            UPDATE students
                            SET grade = ?,
                                specialization = ?
                            WHERE id = ?
                            LIMIT 1
                          """,
            (grade, new_specialization, id),
        )
        Student.db.commit()

        # translate changed the values from numeric and english to arabic.
        new_specialization = translate(new_specialization)
        old["specialization"] = translate(old["specialization"])
        
        old["grade"] = translate(grade)
        grade = translate(grade)
        
        
        # Student Changed Both Grade and Specialization
        if old["grade"] == grade and old["specialization"] == new_specialization:
                    return f"تم تغيير السنة الدراسية من {old['grade']} الي {grade} و التخصص تغير من {old['specialization']} الي {new_specialization}"
                
        # Student Changed Specialization only
        if old["grade"] == grade and old["specialization"] != new_specialization:
            return f"تم تغيير تخصصك من {old['specialization']} الي {new_specialization}"

        # Student Changed Grade Only
        if old["grade"] != grade and old["specialization"] == new_specialization:
            return f"تم تغيير السنة الدراسية من {old['grade']} الي {grade}"
        

    def fetch(id: int) -> dict:
        """Returns The Data Of The Student

        Args:
            id (int): id of the student in the database

        Returns:
            dict: The Data of the student
        """
        return fetch_as_dict(
            Student.c,
            f"SELECT name, grade, specialization FROM students WHERE id = ?",
            id,
        )[0]
