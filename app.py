from flask import Flask, render_template, request
from flask_session import Session
from helpers.myFuncs import give_error, login_required
from helpers.student import Student

app = Flask(__name__)


# configuring Sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    """Outputs the homepage and saves user's data in The database"""
    if request.method == "GET":
        return render_template("index.html")
    args = request.form
    try:
        student = Student(**args)
    except (TypeError, ValueError) as er:
        return give_error(str(er))
    student.add()
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit_specialization():
    """ allows students to edit their data"""
    data = {
        "name": request.form.get("name"),
        "password" : request.form.get("password"),
        "national_id": request.form.get("national_id")
    }
    if Student.isexist(data) is False:
        give_error("الطالب لا يوجد في قاعدة البيانات")


app.run(debug=True)
