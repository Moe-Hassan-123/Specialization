import sqlite3
from re import fullmatch
from regex import P
from werkzeug.security import check_password_hash, generate_password_hash


class Student:
    """
    A class that stores students in a database and allow mutiple function on them.
    """

    db = sqlite3.connect("students.db")
    cur = db.cursor()

    def __init__(
        self,
        name: str,
        national_id: str,
        password: str,
        grade: int,
        specialization: str,
    ):
        """
        It Creates the student in the database.
        """
        Student.cur.execute(
            "INSERT INTO students(name,password,national_id,grade,specialization) Values(?,?,?,?,?)",
            (
                name,
                generate_password_hash(password),
                generate_password_hash(national_id),
                grade,
                specialization,
            ),
        )
        self._id = self.cur.lastrowid
        Student.db.commit()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        # got this pattern from RockOnGom's comment on stackoverflow(https://stackoverflow.com/a/5142164)
        # minimum 8 letters and at least one (number, lowercase letter, uppercase letter and special character) 
        pattern = (
            r"(?=.*([A-Z]){1,})(?=.*[!@#$&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,100}"
        )
        if fullmatch(pattern, password) is None:
            raise ValueError("Weak Password")
        self._password = generate_password_hash(password)

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, national_id):
        # check if it follows the format
        if (
            fullmatch(r"(2|3)\d{4}([1-9]|[12][0-9]|3[01])\d{6}[1-9]", national_id)
            is None
        ):
            raise ValueError("Incorrect National Id")
        self._national_id = generate_password_hash(national_id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        # this pattern matches 3 arabic words with a single space inbetween
        pattern = r"(?:[\u0621-\u064A]+ ){2}[\u0621-\u064A]+"
        if fullmatch(pattern, name) is None:
            raise ValueError(
                'Should Provide a Full Name in Arabic\n Example: "محمد حسن محمد"'
            )
        self._name = name

    @property
    def grade(self):
        return self.grade
    
    @grade.setter
    def grade(self, grade: int):
        if grade not in [11,12]:
            raise ValueError("Grade Must be 11 or 12")
        self._grade = grade
    
    def add_to_database(self):
        ...
