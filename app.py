from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
import os

# Load .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Read PDF
pdf_path = "data/college-dataset.pdf"

reader = PdfReader(pdf_path)

college_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        college_text += text + "\n"

print("College PDF loaded successfully.")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        question = data.get("message", "").strip()

        if not question:
            return jsonify({
                "reply": "Please enter a question."
            })

        prompt = f"""
You are a college information chatbot for
St. Joseph's College (Autonomous), Devagiri, Kozhikode.

Answer the student's question using ONLY the information
provided in the college document below.

Do not make up information.

If the answer is not available in the document, say:

"Sorry, I don't have that information in my college database."

Give a simple and clear answer.

COLLEGE DOCUMENT:

{college_text}

STUDENT QUESTION:

{question}
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        answer = response.text

        return jsonify({
            "reply": answer
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "reply": "Sorry, something went wrong."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)