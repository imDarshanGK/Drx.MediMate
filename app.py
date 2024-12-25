import json
import google.generativeai as genai
from flask import Flask, render_template, request

# Configure API key for Gemini
genai.configure(api_key='Gemini_key')
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Initialize Flask app
app = Flask(__name__)

# Function to get drug information
def get_drug_information(drug_name):
    prompt = f"Provide a clinical summary for pharmacists on the drug {drug_name}. Include its therapeutic uses, standard dosage guidelines, common and serious side effects, contraindications, and important drug interactions. Focus on details relevant for medical decision-making, emphasizing efficient and safe use for patient care."
    response = model.generate_content(prompt)
    return response.text

# Function to check symptoms and recommend drugs
def symptom_checker(symptoms):
    prompt = f"Given these symptoms: {symptoms}, suggest evidence-based, over-the-counter treatment options. Include possible side effects, drug interactions, and safety information to guide pharmacists. Ensure that the suggestions prioritize patient safety and reflect the latest clinical guidelines. Emphasize that this is for educational reference only and not a substitute for professional diagnosis."
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def sisu():
    return render_template('sisu.html')

@app.route('/index.html')
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
