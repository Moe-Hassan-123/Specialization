from flask import render_template,redirect, url_for,session
from functools import wraps

def give_output(message) -> None:
    return render_template("output.html", message=message)


# FROM https://www.codegrepper.com/code-examples/python/python+cursor+fetchall+to+dictionary
def fetch_as_dict(cursor, cursorQuery: str, *params) -> dict:
    """Graps Data from sqlite3 database in the form of a dictionary

    Args:
        cursor (Cursor): The connection to the sqlite3 database.
        cursorQuery (str): The query to be run on the database.

    Returns:
        dict: the result of the query in the form of a dictionary.
    """
    cursor.execute(cursorQuery, params)
    records = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append(dict(zip(columnNames, record)))
    return insertObject


def login_required(f):
    """
        Decorate routes to require login.
        https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def translate(val :str | int) -> str:
    """Changes Values from numeric and english to understandable arabic values.

    Args:
        val (str | int): Value that should be changed

    Returns:
        str: The Translated Understandable Value
    """
    match val:
        case "s":
            return "علمي"
        case "l":
            return "أدبي"
        case "m":
            return "علمي رياضة"
        case "o":
            return "علمي علوم"
        case 2:
            return "ثالثة ثانوي"
        case 1:
            return "تانية ثانوي"
    raise ValueError("UNKOWN")