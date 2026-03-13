from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

model = joblib.load("career_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# HOME ROUTE
@app.route("/")
def home():
    return "Career AI Backend Running"

# REGISTER API
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(name,email,password) VALUES(?,?,?)",
        (name, email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User Registered Successfully"})

# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login Success", "user_id": user[0]})
    else:
        return jsonify({"message": "Invalid Login"})


#ASSESSMENT API
@app.route("/assessment", methods=["POST"])
def assessment():

    data = request.json
    user_id = data["user_id"]

    R = data["q1"] + data["q2"] + data["q3"]
    I = data["q4"] + data["q5"] + data["q6"]
    A = data["q7"] + data["q8"] + data["q9"]
    S = data["q10"] + data["q11"] + data["q12"]
    E = data["q13"] + data["q14"] + data["q15"]
    C = data["q16"] + data["q17"] + data["q18"]

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO assessment(user_id,R,I,A,S,E,C) VALUES(?,?,?,?,?,?,?)",
        (user_id,R,I,A,S,E,C)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message":"Assessment Saved",
        "RIASEC":{
            "R":R,"I":I,"A":A,"S":S,"E":E,"C":C
        }
    })


#PREDICTION API
@app.route("/predict_career", methods=["POST"])
def predict_career():

    data = request.json

    R = data["R"]
    I = data["I"]
    A = data["A"]
    S = data["S"]
    E = data["E"]
    C = data["C"]

    interest = data["interest"]   # student's preferred career

    input_data = np.array([[R,I,A,S,E,C]])

    probs = model.predict_proba(input_data)[0]

    careers = encoder.classes_

    result = {}

    for i in range(len(careers)):
        result[str(careers[i])] = float(round(float(probs[i]) * 100, 2))

    # FINAL INTELLIGENT LOGIC
    best_model_career = str(careers[np.argmax(probs)])

    if interest == best_model_career:
        final = "Perfect Match"
    else:
        final = "Interest-Model Mismatch → Skill Gap Guidance Needed"

    return jsonify({
        "probabilities": result,
        "model_recommendation": best_model_career,
        "interest_analysis": final
    })


#Skill gap route
@app.route("/skill_gap", methods=["POST"])
def skill_gap():

    data = request.json

    career = data["career"]

    python = data["python"]
    maths = data["maths"]
    communication = data["communication"]

    if career == "Engineering":

        gap = (10-python) + (10-maths)

        if gap > 10:
            level = "Beginner"
        elif gap > 5:
            level = "Intermediate"
        else:
            level = "Advanced"

    elif career == "Lawyer":

        gap = (10-communication) + (10-maths)

        if gap > 10:
            level = "Beginner"
        elif gap > 5:
            level = "Intermediate"
        else:
            level = "Advanced"

    else:
        level = "General Path"

    return jsonify({
        "gap_score": gap,
        "recommended_level": level
    })


#RECOMMENDATION COURSE API
@app.route("/recommend_courses", methods=["POST"])
def recommend_courses():

    data = request.json

    career = data["career"]
    level = data["level"]

    courses = []

    if career == "Engineering":

        if level == "Beginner":
            courses = [
                "Python Basics – Coursera",
                "Maths for Engineers – Khan Academy",
                "Problem Solving – HackerRank"
            ]

        elif level == "Intermediate":
            courses = [
                "Data Structures – Udemy",
                "Engineering Mathematics – NPTEL",
                "System Design Basics – Coursera"
            ]

        else:
            courses = [
                "Advanced AI – Coursera",
                "Cloud Engineering – AWS",
                "Competitive Programming – Codeforces"
            ]

    elif career == "Lawyer":

        if level == "Beginner":
            courses = [
                "Introduction to Law – Coursera",
                "Legal Writing – edX",
                "Public Speaking – Udemy"
            ]

        elif level == "Intermediate":
            courses = [
                "Corporate Law – Coursera",
                "Legal Research – edX",
                "Negotiation Skills – Udemy"
            ]

        else:
            courses = [
                "International Law – Coursera",
                "Advanced Litigation – edX",
                "Legal Strategy – Harvard Online"
            ]

    else:
        courses = ["General Career Development – Coursera"]

    return jsonify({
        "recommended_courses": courses
    })


#FUTURE SIMULATION API
@app.route("/career_simulation", methods=["POST"])
def career_simulation():

    data = request.json

    career = data["career"]
    level = data["level"]

    if career == "Engineering":

        if level == "Beginner":
            salary_path = [300000, 500000, 800000, 1200000]

        elif level == "Intermediate":
            salary_path = [500000, 800000, 1400000, 2000000]

        else:
            salary_path = [800000, 1500000, 2500000, 4000000]

    elif career == "Lawyer":

        if level == "Beginner":
            salary_path = [250000, 400000, 700000, 1000000]

        elif level == "Intermediate":
            salary_path = [400000, 700000, 1200000, 1800000]

        else:
            salary_path = [700000, 1400000, 2500000, 3500000]

    else:
        salary_path = [200000, 300000, 500000, 800000]

    stages = ["Entry Level", "Junior", "Mid Level", "Senior"]

    return jsonify({
        "career": career,
        "growth_stages": stages,
        "salary_projection": salary_path
    })

#PREDICTION EXPLANATION API
@app.route("/explain_prediction", methods=["POST"])
def explain_prediction():

    data = request.json

    R = data["R"]
    I = data["I"]
    A = data["A"]
    S = data["S"]
    E = data["E"]
    C = data["C"]

    scores = {
        "Realistic": R,
        "Investigative": I,
        "Artistic": A,
        "Social": S,
        "Enterprising": E,
        "Conventional": C
    }

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    top_factor = sorted_scores[0][0]

    return jsonify({
        "top_influencing_factor": top_factor,
        "full_score_analysis": scores
    })


#FUTURE CAREER GUIDANCE API
@app.route("/full_career_guidance", methods=["POST"])
def full_career_guidance():

    data = request.json

    R = data["R"]
    I = data["I"]
    A = data["A"]
    S = data["S"]
    E = data["E"]
    C = data["C"]
    interest = data["interest"]

    input_data = np.array([[R,I,A,S,E,C]])

    probs = model.predict_proba(input_data)[0]
    careers = encoder.classes_

    result = {}

    for i in range(len(careers)):
        result[str(careers[i])] = float(round(float(probs[i])*100,2))

    best_model_career = str(careers[np.argmax(probs)])

    # interest logic
    if interest == best_model_career:
        match = "Perfect Match"
    else:
        match = "Interest mismatch – improvement roadmap required"

    # skill gap simple logic
    gap_score = (100 - max(result.values()))/10

    if gap_score > 5:
        level = "Beginner"
    elif gap_score > 2:
        level = "Intermediate"
    else:
        level = "Advanced"

    return jsonify({
        "career_probabilities": result,
        "model_recommendation": best_model_career,
        "interest_analysis": match,
        "skill_gap_level": level
    })

if __name__ == "__main__":
    print("Career AI Backend Running")
    app.run(debug=True, port=5000)
