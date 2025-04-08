import os
import json
import base64
from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# Load Gemini API key
api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Initialize Flask app
app = Flask(__name__)

# Function: Get drug info from text
def get_drug_information(drug_name):
    prompt = f"""Provide a clinical summary for pharmacists on the drug {drug_name}.
Include therapeutic uses, standard dosage, common & serious side effects, contraindications, and important drug interactions.
Focus on safe & efficient patient care."""
    response = model.generate_content(prompt)
    return response.text

# Function: Recommend drugs based on symptoms
def symptom_checker(symptoms):
    prompt = f"""Given the symptoms: {symptoms}, recommend over-the-counter treatment options.
Include side effects, interactions, and safety tips for pharmacists. 
Clarify this is educational and not a substitute for diagnosis."""
    response = model.generate_content(prompt)
    return response.text

# Function: Analyze medicine image using Gemini Vision
def analyze_image_with_gemini(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))
    gemini_image = {
        "mime_type": "image/png",
        "data": image
    }
    prompt = """Analyze this image of a medicine or drug packaging. Identify the drug name, manufacturer (if visible), and give a brief summary.
Only answer if the image is clear. If not, politely ask the user to retake the image."""
    response = model.generate_content([prompt, gemini_image])
    return response.text

# Routes
@app.route('/')
def sisu():
    return render_template('sisu.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/drug-info-page')
def drug_info_page():
    return render_template('drug_info.html')

@app.route('/symptom-checker-page')
def symptom_checker_page():
    return render_template('symptom_checker.html')

@app.route('/upload-image-page')
def upload_image_page():
    return render_template('upload_image.html')

# AJAX drug info
@app.route('/get_drug_info', methods=['POST'])
def get_drug_info():
    data = request.get_json()
    drug_name = data.get('drug_name')
    response = get_drug_information(drug_name)
    return json.dumps({'response': response})

# AJAX symptom checker
@app.route('/symptom_checker', methods=['POST'])
def symptom_check():
    data = request.get_json()
    symptoms = data.get('symptoms')
    response = symptom_checker(symptoms)
    return json.dumps({'response': response})

# POST route for uploaded image
@app.route('/process-upload', methods=['POST'])
def process_upload():
    image_data = request.form.get("image_data")
    if image_data:
        try:
            result = analyze_image_with_gemini(image_data)
            return render_template("upload_image.html", result=result)
        except Exception as e:
            return render_template("upload_image.html", result="❌ Error analyzing image: " + str(e))
    return render_template("upload_image.html", result="❌ No image data received.")

if __name__ == '__main__':
    app.run(debug=True)
