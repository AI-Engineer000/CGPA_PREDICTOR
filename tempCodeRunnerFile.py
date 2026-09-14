# app.py
import os
from flask import Flask, render_template, request
from model import analyze_student

app = Flask(__name__)

# Home page


@app.route("/")
def home():
    return render_template("index.html")

# Predict route (POST method)


@app.route("/predict", methods=["POST"])
def predict():
    # Form inputs
    attendance = float(request.form.get("attendance", 0))
    prevcgpa = float(request.form.get("prevcgpa", 0))

    sub1 = float(request.form.get("sub1", 0))
    sub2 = float(request.form.get("sub2", 0))
    sub3 = float(request.form.get("sub3", 0))
    sub4 = float(request.form.get("sub4", 0))
    sub5 = float(request.form.get("sub5", 0))

    name1 = request.form.get("name1", "")
    name2 = request.form.get("name2", "")
    name3 = request.form.get("name3", "")
    name4 = request.form.get("name4", "")
    name5 = request.form.get("name5", "")

    data = [attendance, prevcgpa, sub1, sub2, sub3, sub4, sub5]
    subjects = [name1, name2, name3, name4, name5]

    # Analyze
    predicted, category, weak, suggestions, improved = analyze_student(
        data, subjects)

    # Render index.html with results
    return render_template(
        "index.html",
        predicted=predicted,
        category=category,
        weak=weak,
        suggestions=suggestions,
        improved=improved,

        attendance=attendance,
        prevcgpa=prevcgpa,

        name1=name1,
        name2=name2,
        name3=name3,
        name4=name4,
        name5=name5,

        sub1=sub1,
        sub2=sub2,
        sub3=sub3,
        sub4=sub4,
        sub5=sub5,
    )


# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
