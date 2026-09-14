# CGPA Predictor

A Flask-based student CGPA prediction web app that helps users estimate their future CGPA based on attendance, previous CGPA, and current semester SGPA.

## Features

- User signup and login
- Student authentication using SQLite
- Branch and semester subject selection
- SGPA calculation
- CGPA prediction using a linear regression model
- Performance category and improvement suggestions
- Simple responsive HTML dashboard

## Tech Stack

- Python
- Flask
- SQLite
- scikit-learn
- NumPy
- HTML/CSS/JavaScript

## Project Structure

```text
CGPA_PREDICTOR/
├── app.py
├── model.py
├── requirements.txt
├── .gitignore
├── students.db
├── data/
│   ├── AI.json
│   ├── CSE.json
│   └── IT.json
├── templates/
│   ├── index.html
│   ├── login.html
│   └── signup.html
└── README.md
```

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/AI-Engineer000/CGPA_PREDICTOR.git
cd CGPA_PREDICTOR
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python app.py
```

5. Open in browser:

```text
http://127.0.0.1:5000
```

## Usage

- Sign up with a new account
- Log in using your username and password
- Select your branch and semester
- Enter your marks for each subject
- Submit the form to view predicted CGPA and suggestions

## Notes

- The app stores user accounts in SQLite.
- The prediction model is trained using sample data in `model.py`.
- The subject data is stored in JSON files under `data/`.

## License

This project is for educational and learning purposes.
