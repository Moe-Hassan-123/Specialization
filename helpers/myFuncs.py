from sqlite3 import Cursor
from flask import redirect, render_template, request, session
from sqlite3 import Cursor

# FROM CS50x Finance problem set
def give_error(message: str, code: int = 400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", top=code, bottom=escape(message))


def give_success(message: str = "تم بنجاح!") -> None:
    return render_template("success.html", message=message)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# FROM https://www.codegrepper.com/code-examples/python/python+cursor+fetchall+to+dictionary
def fetch_as_dict(cursor: Cursor, cursorQuery: str) -> dict:
    cursor.execute(cursorQuery)
    records = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append(dict(zip(columnNames, record)))
    return insertObject
