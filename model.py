# model.py
import numpy as np
from sklearn.linear_model import LinearRegression
X = np.array([
    [60, 6.0, 6.5],
    [75, 7.2, 7.8],
    [85, 8.0, 8.5],
    [90, 9.0, 9.2],
    [50, 5.5, 6.0],
    [70, 6.8, 7.2],
    [80, 7.5, 8.0],
    [65, 6.5, 7.0],
    [55, 5.8, 6.3],
    [88, 8.7, 9.0],
    [92, 9.2, 9.5],
    [78, 7.8, 8.3]
])
y = np.array([
    6.7, 7.9, 8.6, 9.3, 6.2, 7.3, 8.1, 7.1, 6.4, 9.1, 9.6, 8.4
])
y = y + np.random.normal(0, 0.1, len(y))

model = LinearRegression()
model.fit(X, y)


def analyze_student(data, subjects):
    """
    data = [attendance, prevcgpa, sgpa]
    subjects = list of subject names
    """

    attendance = float(data[0])
    prevcgpa = float(data[1])
    sgpa = float(data[2])

    # PREDICTION
    input_data = np.array([[attendance, prevcgpa, sgpa]])
    predicted = model.predict(input_data)[0]
    predicted = round(predicted, 2)
    if predicted > 10:
        predicted = 10
    if predicted < 0:
        predicted = 0

    # CATEGORY
    if predicted >= 9:
        category = "Excellent Performer"
    elif predicted >= 8:
        category = "Good Performer"
    elif predicted >= 7:
        category = "Average Performer"
    else:
        category = "Needs Improvement"

    # WEAK SUBJECTS
    weak = []
    if sgpa < 6.5:
        weak = subjects[:2]  # assume first 2 weak
    elif sgpa < 8:
        weak = subjects[:1]

    # SUGGESTIONS
    suggestions = []

    if attendance < 75:
        suggestions.append("Increase attendance for better understanding.")

    if sgpa < 7:
        suggestions.append(
            "Focus more on weak subjects and practice regularly.")

    if predicted < 7:
        suggestions.append("Improve consistency in studies.")

    if prevcgpa > sgpa:
        suggestions.append(
            "Your performance has dropped compared to your previous CGPA. Focus on consistency and weak subjects.")
    elif prevcgpa < sgpa:
        suggestions.append(
            "Great improvement from your previous CGPA! You're performing better than before. Keep it up!")
    else:
        suggestions.append(
            "Your performance is stable. Aim for continuous improvement.")
    # IMPROVED CGPA
    improved = round(predicted + 0.5, 2)
    if improved > 10:
        improved = 10
    return predicted, category, weak, suggestions, improved
