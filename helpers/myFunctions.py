from sqlite3 import Cursor
from flask import render_template

def give_output(message: str = "Unkown error occured \n Please Contact us for help\n Email: Mdhn6832@gmail.com") -> None:
    return render_template("output.html", message=message)

# FROM https://www.codegrepper.com/code-examples/python/python+cursor+fetchall+to+dictionary
def fetch_as_dict(cursor: Cursor, cursorQuery: str) -> dict:
    cursor.execute(cursorQuery)
    records = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append(dict(zip(columnNames, record)))
    return insertObject
