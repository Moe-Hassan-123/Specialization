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
    print(test_student())
