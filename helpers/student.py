import sqlite3
from re import fullmatch
from regex import P
from validator_collection import none
from werkzeug.security import check_password_hash, generate_password_hash


class Student:
    """
    A class that stores students in a database and allow mutiple function on them.
    """

    def __init__(self, name, password, national_id, grade, specialization):
        """
        It Creates a link to the database
        """
        self.name = name
        self.password = password
        self.national_id = national_id
        self.grade = grade
        self.specialization = specialization
        self.db = sqlite3.connect("students.db")
        self.c = self.db.cursor()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if type(password) is not str:
            raise (TypeError)
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
    def national_id(self, national_id: str):
        # check if it follows the format
        if type(national_id) is not str:
            raise (TypeError)
        if (
            fullmatch(r"(2|3)\d{4}([1-9]|[12][0-9]|3[01])\d{6}[1-9]", national_id)
            is None
        ):
            raise ValueError("Incorrect National Id")
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
            raise ValueError(
                'Should Provide a Full Name in Arabic\n Example: "محمد حسن محمد"'
            )
        self._name = name

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade: int):
        if grade not in [11, 12]:
            raise ValueError("Grade Must be 11 or 12")
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
            raise ValueError("Invalid Specialization")
        self._specialization = specialization

    def add(self):
        ### TODO:
        ### try to check if all values we need exist
        values = {
            "name": self.name,
            "password": self.password,
            "national_id": self.national_id,
            "grade": self.grade,
            "specialization": self.specialization,
        }
        for key in values:
            if values[key] is None:
                raise ValueError("Missing Parameters")
        self.c.execute(
            "SELECT national_id FROM students WHERE name = ? AND grade = ? AND specialization = ?",
            [self.name, self.grade, self.specialization],
        )
        for national_id in self.c.fetchall():
            if check_password_hash(self.national_id, national_id) == False:
                raise ValueError("National Id already registered")
        self.c.execute(
            """INSERT INTO students   (name,
                                      password,
                                      national_id,
                                      grade,
                                      specialization)
                                      Values(?,?,?,?,?)""",
            [
                self.name,
                self.password,
                self.national_id,
                generate_password_hash(self.grade),
                self.specialization,
            ],
        )
        if self.c.lastrowid is None:
            raise ValueError("insert didnt work")
