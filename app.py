from distutils.command.build_scripts import first_line_re
from flask import Flask, render_template, request
from flask_session import Session
from student import Student
from myFuncs import login_required
from werkzeug.security import check_password_hash, generate_password_hash

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
    """Register Function That allows the users to save thier data in The database"""
    if request.method == "GET":
        return render_template("register.html")
    student = Student(
        first=request.form.get("first"),
        last=request.form.get("last"),
        national_id=generate_password_hash(request.form.get("national_id")),
        password=generate_password_hash(request.form.get("password")),
        specialization=request.form.get("specialization"),
    )


@app.route("/specialize", methods=["GET", "POST"])
@login_required
def specialize():
    """Specialize allows students to save their learning prefrences on which subjects they wish  to study"""
    ...


app.run(debug=True)
