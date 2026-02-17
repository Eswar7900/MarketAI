from flask import Flask, render_template, request, jsonify
import requests
import os
import sqlite3
import datetime
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("marketai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            input TEXT,
            result TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- AI FUNCTION ----------------
def call_groq(prompt):
    try:
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(GROQ_URL, headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return "Error: AI response failed. Check API key."

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error calling AI: {str(e)}"


# ---------------- SAVE TO DB ----------------
def save_to_db(request_type, user_input, result):
    conn = sqlite3.connect("marketai.db")
    cursor = conn.cursor()

    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO history (type, input, result, created_at) VALUES (?, ?, ?, ?)",
        (request_type, user_input, result, created_at)
    )

    conn.commit()
    conn.close()


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/campaign")
def campaign():
    return render_template("campaign.html")


@app.route("/sales")
def sales():
    return render_template("sales.html")


@app.route("/lead")
def lead():
    return render_template("lead.html")


# ---------------- CAMPAIGN AI ----------------
@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    data = request.json
    product = data.get("product")

    prompt = f"""
    Create a professional marketing campaign for {product}.
    Include:
    - Objectives
    - 5 content ideas
    - 3 ad copies
    - Call to action
    """

    result = call_groq(prompt)
    save_to_db("campaign", product, result)

    return jsonify({"result": result})


# ---------------- SALES AI ----------------
@app.route("/generate_sales", methods=["POST"])
def generate_sales():
    data = request.json
    product = data.get("product")

    prompt = f"""
    Create a powerful sales pitch for {product}.
    Include:
    - 30-second pitch
    - Value proposition
    - Differentiators
    - Closing line
    """

    result = call_groq(prompt)
    save_to_db("sales", product, result)

    return jsonify({"result": result})


# ---------------- LEAD AI ----------------
@app.route("/score_lead", methods=["POST"])
def score_lead():
    data = request.json
    name = data.get("name")

    prompt = f"""
    Score this sales lead from 0-100.

    Lead Details:
    {name}

    Provide:
    - Lead score
    - Reasoning
    - Conversion probability
    """

    result = call_groq(prompt)
    save_to_db("lead", name, result)

    return jsonify({"result": result})


# ---------------- HISTORY PAGE ----------------
@app.route("/history")
def history():
    conn = sqlite3.connect("marketai.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    records = cursor.fetchall()

    conn.close()

    return render_template("history.html", records=records)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
