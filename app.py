import os
import json
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import markdown

# ---------------------------
# Configuration & Setup
# ---------------------------

# Load Gemini API key from environment variable
api_key = os.getenv("GEMINI_KEY")
if not api_key:
    raise EnvironmentError("❌ GEMINI_KEY environment variable not set.")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# ---------------------------
# Utility
# ---------------------------

def api_response(message, status=200):
    """Standard JSON response helper"""
    return jsonify({'response': message}), status

def format_markdown_response(text):
    """Convert Markdown text to HTML for consistent, readable output"""
    if not text or text.startswith("❌"):
        return text  # Return error messages as-is
    # Convert Markdown to HTML
    html = markdown.markdown(text, extensions=['extra', 'fenced_code'])
    # Wrap in a styled div for better presentation
    return f'<div class="markdown-content">{html}</div>'

# ---------------------------
# AI Functions
# ---------------------------

def get_drug_information(drug_name):
    prompt = (
        f"Provide a brief clinical summary for pharmacists on the drug **{drug_name}** in Markdown format:\n"
        "## Therapeutic Uses\n"
        "- List primary therapeutic uses\n"
        "## Standard Dosage\n"
        "- Provide standard adult dosage (include administration route and frequency)\n"
        "## Common Side Effects\n"
        "- List common side effects\n"
        "## Serious Side Effects\n"
        "- List serious side effects requiring immediate attention\n"
        "## Contraindications\n"
        "- List conditions or scenarios where the drug should not be used\n"
        "## Important Drug Interactions\n"
        "- List significant drug interactions\n"
        "Use concise bullet points. Ensure clarity and professional tone."
    )
    response = model.generate_content(prompt)
    text = response.text.strip() if response and hasattr(response, 'text') else "❌ No response from AI."
    return format_markdown_response(text)

def get_symptom_recommendation(symptoms):
    prompt = (
        f"Given the symptoms: **{symptoms}**, recommend over-the-counter treatment options in Markdown format:\n"
        "## Recommended Over-the-Counter Treatments\n"
        "- List appropriate OTC medications or treatments\n"
        "## Common Side Effects\n"
        "- List common side effects of recommended treatments\n"
        "## Important Interactions\n"
        "- List significant drug or condition interactions\n"
        "## Safety Tips\n"
        "- Provide key safety tips or precautions\n"
        "If symptoms suggest a medical emergency or severe condition, clearly state: **'Seek immediate medical attention.'** "
        "Use concise bullet points in Markdown format. Avoid disclaimers."
    )
    response = model.generate_content(prompt)
    text = response.text.strip() if response and hasattr(response, 'text') else "❌ No response from AI."
    return format_markdown_response(text)

def analyze_image_with_gemini(image_data):
    try:
        if not image_data.startswith("data:image/"):
            return "❌ Invalid image format uploaded."

        image_base64 = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes))

        prompt = (
            "Analyze this image of a medicine or drug packaging. Provide the response in Markdown format:\n"
            "## Drug Information\n"
            "- **Drug Name**: Identify the drug name (if visible)\n"
            "- **Manufacturer**: Identify the manufacturer (if visible)\n"
            "## Clinical Summary\n"
            "- **Therapeutic Uses**: List primary uses\n"
            "- **Standard Dosage**: Provide standard dosage\n"
            "- **Common Side Effects**: List common side effects\n"
            "- **Serious Side Effects**: List serious side effects\n"
            "- **Contraindications**: List contraindications\n"
            "- **Important Interactions**: List significant interactions\n"
            "If the image is blurry or unclear, respond with: **'Please retake the image for better clarity.'**"
        )

        response = model.generate_content([prompt, image])
        text = response.text.strip() if response and hasattr(response, 'text') else "❌ Analysis failed or empty response from AI."
        return format_markdown_response(text)

    except Exception as e:
        return f"❌ Error during image analysis: {str(e)}"

# ---------------------------
# Routes (Pages)
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

@app.route('/get_drug_info', methods=['POST'])
def get_drug_info():
    try:
        data = request.get_json()
        drug_name = data.get('drug_name')
        if not drug_name:
            return api_response('❌ No drug name provided.', 400)
        response = get_drug_information(drug_name)
        return api_response(response)
    except Exception as e:
        return api_response(f"❌ Error: {str(e)}", 500)

@app.route('/symptom_checker', methods=['POST'])
def symptom_check():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms')
        if not symptoms:
            return api_response('❌ No symptoms provided.', 400)
        result = get_symptom_recommendation(symptoms)
        return api_response(result)
    except Exception as e:
        return api_response(f'❌ Error during analysis: {str(e)}', 500)

@app.route('/process-upload', methods=['POST'])
def process_upload():
    image_data = request.form.get("image_data")
    if image_data:
        result = analyze_image_with_gemini(image_data)
        return render_template("upload_image.html", result=result)
    return render_template("upload_image.html", result="❌ No image data received.")

@app.route('/my-account')
def my_account():
    return render_template('my_account.html', user={
        "name": "Demo User",
        "email": "demo@example.com",
        "notifications": True
    })

# ---------------------------
# Run app
# ---------------------------

if __name__ == '__main__':
    # Use FLASK_DEBUG=true in your environment to enable debug mode
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")