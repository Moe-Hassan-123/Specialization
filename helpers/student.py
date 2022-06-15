import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


class Student:
    """
    A class that stores students in a database and allow mutiple function on them.
    """

    db = sqlite3.connect("students.db")

    def __init__(
        self,
        first: str,
        last: str,
        national_id: bytes,
        password: bytes,
        grade: int,
        specialization: str,
    ):
        """
        It Creates the student in the database.
        """
        self.db = sqlite3.connect("students.db")
        self.cur = self.db.cursor()
        self.name = f"{first} {last}"
        self.cur.execute("SELECT national_id FROM students")
        for hashed_id in self.cur.fetchall():
            if check_password_hash(hashed_id[0],national_id) == True:
                print("User Exists Already")
                self.cur.execute("SELECT ")
                return
            
        self.cur.execute(
            "INSERT INTO students(name,password,national_id,specialization) Values(?,?,?,?)",
            (self.name,password, generate_password_hash(national_id), specialization),
        )
        self._id = self.cur.lastrowid
        print(self.cur.lastrowid)
        self.db.commit()
        specialization: str,
    ):
        """
        It Creates the student in the database and stores his hashed national_id for other functions
        """
        Student.db.execute(
            "INSERT INTO students(name,password,national_id,specialization) Values(?,?,?,?)",
            (f"{first} {last}", password, national_id, specialization),
        )
        Student.db.commit()
        self._id = national_id

    @property
    def password(self):
        curs = Student.db.cursor()
        curs.execute("SELECT password FROM students WHERE national_id = ?",[self._id])
        return curs.fetchone()[0]

    @password.setter
    def password(cls):
        ...
    
    @property
    def id(self):
        return self._id


def test_student():
    values = {
        "first" : "mohamed",
        "last" : "hassan",
        "password" : generate_password_hash("12345"),
        "national_id" : "3051232156488",
        "grade" : 11,
        "specialization" : "scientific",
    }
    student = Student(**values)
    values = [
        "mohamed",
        "hassan",
        generate_password_hash("hi"),
        generate_password_hash("hello"),
        "scientific",
    ]
    student = Student(*values)
    return


if __name__ == "__main__":
    test_student()
