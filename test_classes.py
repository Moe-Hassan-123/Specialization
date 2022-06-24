from helpers.student import Student
from pytest import raises
from contextlib import contextmanager
from werkzeug.security import check_password_hash


# https://stackoverflow.com/a/42327075
# a very neat solution to determine if a function didn't raise an error
@contextmanager
def not_raises(ExpectedException):
    try:
        yield

    except ExpectedException as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")

# Test working_test

working_test = {
    "name": "محمد حسن محمد",
    "password" : "Password1#",
    "national_id": "2121230559955",
    "grade" :11,
    "specialization":"scientific"
}

student = Student(**working_test)

### Tests for setter functions
def test_set_national_id():
    with raises(ValueError):
        student.national_id = "12345"

    with not_raises(ValueError):
        student.national_id = "2121230559955"

def test_set_password():
    with raises(ValueError):
        student.password = "12345"

    with not_raises(ValueError):
        student.password = "Mohamed123#"
    
def test_set_wrong_name():
    with raises(ValueError):
        student.name = "Mohamed Hassan"


def test_set_right_name():
    with not_raises(ValueError):
        student.name = "محمد حسن محمد"

def test_set_wrong_type():
    with raises(TypeError):
        student.name = 1234567
    with raises(TypeError):
        student.password = 1234567
    with raises(TypeError):
        student.national_id = 1234567

### Tests for working_testbase manipulation

def test_repeated_add():
    student.add()
    with raises(ValueError):
        student.add()
        
def test_isexist_wrong_user():
    assert Student.isexist("mohamed","123","12345") == False
        
def test_isexist_right_user():
    Student("يوسف حسن محمد", "Password123#4","2124230552955",11,"scientific").add()
    assert Student.isexist("يوسف حسن محمد", "2124230552955", "Password123#4") != False
    