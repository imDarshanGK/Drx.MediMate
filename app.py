import json
import google.generativeai as genai
from flask import Flask, render_template, request

# Configure API key for Gemini
api_key=${{ secrets.GEMINI_API}}
genai.configure(api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Flask app
app = Flask(__name__)

# Function to get drug information
def get_drug_information(drug_name):
    prompt = f"Provide detailed information on the drug {drug_name} including usage, dosage, side effects, and contraindications."
    response = model.generate_content(prompt)
    return response.text

# Function to check symptoms and recommend drugs
def symptom_checker(symptoms):
    prompt = f"Given these symptoms: {symptoms}, suggest possible over-the-counter medications and include any relevant side-effect information. This is for educational purposes only."
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_drug_info', methods=['POST'])
def get_drug_info():
    data = request.get_json()
    drug_name = data.get('drug_name')
    response = get_drug_information(drug_name)
    return json.dumps({'response': response})

@app.route('/symptom_checker', methods=['POST'])
def symptom_check():
    data = request.get_json()
    symptoms = data.get('symptoms')
    response = symptom_checker(symptoms)
    return json.dumps({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
