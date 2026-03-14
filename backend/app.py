from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import joblib
import numpy as np
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# -------------------------
# APP SETUP
# -------------------------

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

model = joblib.load("career_model.pkl")
encoder = joblib.load("label_encoder.pkl")


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():
    return "Career AI Backend Running"


# -------------------------
# REGISTER
# -------------------------

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


# -------------------------
# LOGIN
# -------------------------

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


# -------------------------
# ASSESSMENT
# -------------------------

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


# -------------------------
# PREDICT CAREER
# -------------------------

@app.route("/predict_career", methods=["POST"])
def predict_career():

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
        result[str(careers[i])] = float(round(probs[i] * 100,2))

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


# -------------------------
# SKILL GAP
# -------------------------

@app.route("/skill_gap", methods=["POST"])
def skill_gap():

    data = request.json

    career = data["career"]
    python = data["python"]
    maths = data["maths"]
    communication = data["communication"]

    gap = 0
    level = "General"

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

    return jsonify({
        "gap_score": gap,
        "recommended_level": level
    })


# -------------------------
# COURSE RECOMMENDATION
# -------------------------

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

        courses = [
            "Introduction to Law – Coursera",
            "Legal Writing – edX",
            "Public Speaking – Udemy"
        ]

    else:
        courses = ["General Career Development – Coursera"]

    return jsonify({
        "recommended_courses": courses
    })


# -------------------------
# SALARY SIMULATION
# -------------------------

@app.route("/career_simulation", methods=["POST"])
def career_simulation():

    data = request.json

    career = data["career"]
    level = data["level"]

    if career == "Engineering":

        if level == "Beginner":
            salary = [300000,500000,800000,1200000]
        elif level == "Intermediate":
            salary = [500000,800000,1400000,2000000]
        else:
            salary = [800000,1500000,2500000,4000000]

    else:
        salary = [200000,300000,500000,800000]

    stages = ["Entry","Junior","Mid","Senior"]

    return jsonify({
        "career": career,
        "growth_stages": stages,
        "salary_projection": salary
    })


# -------------------------
# EXPLAIN AI
# -------------------------

@app.route("/explain_prediction", methods=["POST"])
def explain_prediction():

    data = request.json

    scores = {
        "Realistic": data["R"],
        "Investigative": data["I"],
        "Artistic": data["A"],
        "Social": data["S"],
        "Enterprising": data["E"],
        "Conventional": data["C"]
    }

    top = max(scores, key=scores.get)

    return jsonify({
        "top_influencing_factor": top,
        "full_score_analysis": scores
    })


# -------------------------
# PDF REPORT
# -------------------------

@app.route("/download_report", methods=["POST"])
def download_report():

    data = request.json

    buffer = io.BytesIO()
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Career Guidance Report", styles['Title']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Student: {data['name']}", styles['Normal']))
    elements.append(Paragraph(f"Career: {data['career']}", styles['Normal']))
    elements.append(Paragraph(f"Level: {data['level']}", styles['Normal']))
    elements.append(Paragraph(f"Top Factor: {data['factor']}", styles['Normal']))

    doc = SimpleDocTemplate(buffer)
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="career_report.pdf",
        mimetype="application/pdf"
    )

#CAREER ROADMAP 
@app.route("/career_roadmap", methods=["POST"])
def career_roadmap():

    data = request.json
    career = data["career"]

    roadmap = {
        "Engineering": [
            "Learn Programming (Python / C++)",
            "Study Data Structures & Algorithms",
            "Build Web / Software Projects",
            "Learn Databases and System Design",
            "Apply for internships"
        ],
        "Lawyer": [
            "Study Constitutional Law",
            "Practice Legal Writing",
            "Participate in Moot Courts",
            "Intern at Law Firms",
            "Prepare for Judiciary Exams"
        ]
    }

    return jsonify({
        "career": career,
        "roadmap": roadmap.get(career, ["Explore career paths"])
    })


@app.route("/career_chatbot", methods=["POST"])
def career_chatbot():

    data = request.json
    question = data.get("question","").lower()

    response = ""

    if "engineer" in question or "engineering" in question:
        response = """
To become an Engineer you should follow this roadmap:

1. Learn Programming (Python / Java)
2. Study Data Structures and Algorithms
3. Practice problem solving
4. Work on real world projects
5. Apply for internships
6. Prepare for technical interviews
"""

    elif "data scientist" in question:
        response = """
Data Scientist Career Path:

1. Learn Python
2. Study Statistics and Mathematics
3. Learn Machine Learning
4. Work with datasets using Pandas
5. Build ML projects
6. Learn Deep Learning
"""

    elif "skills" in question:
        response = """
Important skills for career growth:

• Programming (Python / Java)
• Problem Solving
• Communication Skills
• Analytical Thinking
• Team Collaboration
"""

    elif "salary" in question:
        response = """
Typical salary growth:

Entry Level → ₹3L – ₹5L  
Junior → ₹5L – ₹8L  
Mid Level → ₹8L – ₹15L  
Senior → ₹15L – ₹30L+
"""

    elif "roadmap" in question:
        response = """
General Career Roadmap:

Year 1 → Learn Fundamentals  
Year 2 → Build Projects  
Year 3 → Internship + Advanced Skills  
Year 4 → Job Preparation + Portfolio
"""

    elif "courses" in question:
        response = """
Recommended learning platforms:

• Coursera
• Udemy
• edX
• Khan Academy
• NPTEL
"""

    else:
        response = """
I can help with:

• Career guidance
• Skills to learn
• Salary growth
• Career roadmap
• Best courses

Ask me something like:
"What skills should I learn?"
"""

    return jsonify({
        "answer": response
    })

#SKILL PROGRESS TRACKING
@app.route("/skill_progress", methods=["GET"])
def skill_progress():

    progress = {
        "months": ["Jan", "Feb", "Mar", "Apr", "May"],
        "python": [3, 5, 6, 7, 8],
        "maths": [4, 5, 6, 7, 7],
        "communication": [5, 6, 7, 7, 8]
    }

    return jsonify(progress)

#SAVE RESULT TO DB
@app.route("/save_result", methods=["POST"])
def save_result():

    data = request.json

    user_id = data.get("user_id")
    career = data.get("career")
    level = data.get("level")

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            career TEXT,
            level TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO results(user_id, career, level) VALUES(?,?,?)",
        (user_id, career, level)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Result saved successfully"
    })

# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    print("Career AI Backend Running")
    app.run(debug=True, port=5000)