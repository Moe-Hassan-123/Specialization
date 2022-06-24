from flask import Flask, render_template, request
from helpers.myFunctions import give_output
from helpers.student import Student

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    """Outputs the homepage and saves user's data in The database"""
    if request.method == "GET":
        return render_template("index.html")
    args = request.form
    student = Student(**args)
    try:
        output = student.add()
    except AttributeError:
        return give_output("الطالب مسجل من قبل لذا لم يتم تسجيله")
    return give_output(output)

@app.route("/help", methods=["GET"])
def help() -> None:
    """outputs a webpage with a small description of the site and how to use it.
    
    Return: renders a webpage
    """
    
    return render_template("help.html")


@app.route("/delete", methods=["GET", "POST"])
def delete() -> None:
    """Allows users to delete thier entries from the database

    Returns: renders delete.html webpage
    """
    if request.method == "GET":
        return render_template("delete.html")
    # get the data required to locate the user in the database
    data = {
        "name": request.form.get("name"),
        "password": request.form.get("password"),
        "national_id": request.form.get("national_id"),
    }
    # Students.delete returns an output message that shows whethere it was completed succesfully or not.
    return give_output(Student.delete(data))


app.run(debug=True)
