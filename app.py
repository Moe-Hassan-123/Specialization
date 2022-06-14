from flask import Flask, render_template, request
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from student import Student
from myFuncs import login_required

app = Flask(__name__)


# configuring Sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """
    Register Function That allows the users to save thier data in The database
    """
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get()


app.run(debug=True)
