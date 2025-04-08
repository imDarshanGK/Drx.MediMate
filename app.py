import os
import json
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# Load Gemini API key from environment variable
api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize Flask app
app = Flask(__name__)

# ---------------------------
# AI Functions
# ---------------------------

# 1. Get drug info from name
def get_drug_information(drug_name):
    prompt = f"""Provide a clinical summary for pharmacists on the drug {drug_name}.
Include therapeutic uses, standard dosage, common & serious side effects, contraindications, and important drug interactions.
Focus on safe & efficient patient care."""
    response = model.generate_content(prompt)
    return response.text

# 2. Symptom checker (OTC recommendation)
def symptom_checker(symptoms):
    prompt = f"""Given the symptoms: {symptoms}, recommend over-the-counter treatment options.
Include side effects, interactions, and safety tips for pharmacists. 
Clarify this is educational and not a substitute for diagnosis."""
    response = model.generate_content(prompt)
    return response.text

# 3. Analyze medicine image
def analyze_image_with_gemini(image_data):
    try:
        image_base64 = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes))

        prompt = """Analyze this image of a medicine or drug packaging. 
Identify the drug name, manufacturer (if visible), and give a brief clinical summary.
If the image is blurry or unclear, ask the user to retake it politely."""

        # Gemini expects the image object directly
        response = model.generate_content([prompt, image])
        return response.text

    except Exception as e:
        return f"❌ Error during image analysis: {str(e)}"

# ---------------------------
# Routes
# ---------------------------

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

# ---------------------------
# API Endpoints (AJAX/JS)
# ---------------------------

# Drug info from text input
@app.route('/get_drug_info', methods=['POST'])
def get_drug_info():
    try:
        data = request.get_json()
        drug_name = data.get('drug_name')
        if not drug_name:
            return jsonify({'response': '❌ No drug name provided'}), 400
        response = get_drug_information(drug_name)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"❌ Error: {str(e)}"}), 500

# Symptom checker from user input
@app.route('/symptom_checker', methods=['POST'])
def symptom_check():
    data = request.get_json()
    symptoms = data.get('symptoms')
    response = symptom_checker(symptoms)
    return json.dumps({'response': response})


# Analyze uploaded image
@app.route('/process-upload', methods=['POST'])
def process_upload():
    image_data = request.form.get("image_data")
    if image_data:
        result = analyze_image_with_gemini(image_data)
        return render_template("upload_image.html", result=result)
    return render_template("upload_image.html", result="❌ No image data received.")

# ---------------------------
# Run app
# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)
