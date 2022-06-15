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
    """Index Function renders The homepage of The website"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register Function That saves user's data in The database"""
    if request.method == "GET":
        return render_template("register.html")
    args = request.form
    try:
        student = Student(**args)
    except (TypeError, ValueError) as er:
        return give_error(str(er))
    student.add()
    return render_template("register.html")

@app.route("/specialize", methods=["GET", "POST"])
@login_required
def change_specialization():
    """ allows students to edit their learning prefrences on which subjects they wish to study"""
    ...


app.run(debug=True)
