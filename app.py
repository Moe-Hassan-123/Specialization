import PySimpleGUI as sg # Used for a simple GUI
from flask import Flask, render_template, url_for, session, request, redirect
from flask_session import Session
from helpers.myFunctions import give_output, login_required, translate
from helpers.student import Student

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def index(msg=str | None):
    """
    Renders The Home Page.
    """
    return render_template("index.html", msg=msg)


@app.route("/help", methods=["GET"])
def help():
    """
    renders a helping page that shows how to use the site.
    """
    return render_template("help.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders The Register page that allows users to save their data in the database.
    """

    # if they Got there while being logged in we should redirect to profile page.
    if session.get("id"):
        return redirect(url_for("student_profile"))
    
    
    if request.method == "GET":
        return render_template("register.html")


    data = request.form
    try:
        id = Student(**data).id
    except Exception as e:
        return give_output(e)

    # Configure the session to store User's data to allow for quick access during -
    # the session without accessing the database.
    # also the national id is only stored on the session and not in the database

    # The id is the same id the user has in the database which allows for very
    # fast data retrieval for the profile page
    session["id"] = id
    session["name"] = data.get("name")
    session["national_id"] = data.get("national_id")
    return redirect(
        url_for(
            "student_profile", msg="تم التسجيل بنجاح!\n يمكنك تعديل بياناتك او الخروج"
        ),
        code = 307
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""


    # if they Got there while being logged in we should redirect to profile page.
    if session.get("id"):
        return redirect(url_for("student_profile"))
    
    # If they Got there by link then they should Login
    if request.method == "GET":
        return render_template("login.html")


    # Log the student in and
    data = request.form
    if (id := Student.isexist(**data)) is False:
        return give_output("البيانات خاطئة تأكد من الرقم القومي والباسورد")

    # if student exists in the database store the id, name, national id in the session and redirect to his profile
    session["national_id"] = data["national_id"]
    session["name"] = data["name"]
    session["id"] = id
    return redirect(url_for("student_profile", msg="يمكنك تعديل بياناتك!"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def student_profile():
    """
    renders a page that shows The Students registered Data
    """
    id = session.get("id")
    data = Student.fetch(id)
    if request.method == "POST":
        msg = request.args.get("msg")
    else:
        msg = None
    
    return render_template(
        "profile.html",
        grade=translate(data["grade"]),
        specialization=translate(data["specialization"]),
        name=data["name"],
        msg=msg,
    )


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """
    renders a page that allows users to edit their specialization
    """
    if request.method == "GET":
        return render_template("edit.html")

    new_grade = int(request.form.get("grade"))
    new_special = request.form.get("specialization")

    # Check if the grade and specialization are correct
    # protects against people changing the html before requesting the change.
    if (new_grade == 1 and new_special not in ["s", "l"]) or (
        new_grade == 2 and new_special not in ["l", "m", "o"]
    ):
        return redirect(
            url_for(
                "student_profile",
                msg="تخصص وسنة دراسية غير متوافقين"
            ),
            code=307
        )

    return redirect(
        url_for(
            "student_profile",
            msg=Student.edit(session.get("id"), new_special, new_grade),
        ),
        code=307,  # Retains current http method which is POST
    )


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return render_template("index.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', msg="File Not Found", code=404), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
