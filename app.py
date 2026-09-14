import os
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from model import analyze_student

app = Flask(__name__)
app.secret_key = "my_secret_key"

# DATABASE


def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


init_db()


def get_grade_point(marks):
    marks = float(marks)
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks > 40:
        return 5
    elif marks == 40:
        return 4
    else:
        return 0
# -------- SIGNUP --------


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO students (email, username, password) VALUES (?, ?, ?)",
                (email, username, password)
            )
            conn.commit()
        except:
            return "Email or Username already exists!"

        return redirect('/login')   # FIXED

    return render_template('signup.html')

# -------- LOGIN --------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user is not None and check_password_hash(user[3], password):
            session["user"] = user[2]
            return redirect("/")
        else:
            return " Invalid username or password!"

    return render_template('login.html')


# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")


# MAIN DASHBOARD
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")

# -------- FETCHING SUBJECTS ---------


@app.route("/get_subjects", methods=["POST"])
def get_subject():
    data = request.get_json()

    branch = data.get("branch")
    semester = data.get("semester")

    try:
        with open(f"data/{branch}.json") as f:
            subjects_data = json.load(f)

        subjects = subjects_data.get(semester, [])
    except:
        subjects = []

    return jsonify(subjects)


@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect('/login')

    # INPUTS
    attendance = float(request.form.get("attendance", 0))
    prevcgpa = request.form.get("prevcgpa")

    branch = request.form.get("branch")
    semester = request.form.get("semester")

    with open(f"data/{branch}.json") as f:
        subjects_data = json.load(f)

    subjects = subjects_data.get(semester, [])

    marks_list = []
    subjects_names = []

    # MARKS
    for i in range(len(subjects)):
        marks = float(request.form.get(f"marks{i}", 0))
        marks_list.append(marks)
        subjects_names.append(subjects[i]["name"])

    # SGPA CALCULATION
    total = 0
    total_credits = 0

    for i in range(len(subjects)):
        credit = subjects[i]["credit"]
        gp = get_grade_point(marks_list[i])

        total += gp * credit
        total_credits += credit

    sgpa = round(total / total_credits, 2) if total_credits != 0 else 0

    # PREV CGPA FIX
    if not prevcgpa or prevcgpa == "":
        prevcgpa = sgpa
    else:
        prevcgpa = float(prevcgpa)

    # MODEL INPUT
    data = [attendance, prevcgpa, sgpa]

    predicted, category, weak, suggestions, improved = analyze_student(
        data, subjects_names
    )

    # CGPA LIMIT FIX
    predicted = min(predicted, 10)
    improved = min(improved, 10)

    # OUTPUT
    return render_template(
        "index.html",
        predicted=predicted,
        category=category,
        weak=weak,
        suggestions=suggestions,
        improved=improved,

        attendance=attendance,
        prevcgpa=prevcgpa,
        sgpa=sgpa,

        subjects=subjects,
        marks=marks_list
    )


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
