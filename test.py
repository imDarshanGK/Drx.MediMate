import google.generativeai as genai


# Configure API key
genai.configure(api_key="AIzaSyDMRigxIecZge3rI8Y7_PhHu5_bz_mvz1Y")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get drug information
def get_drug_information(drug_name):
    prompt = f"Provide detailed information on the drug {drug_name} including usage, dosage, side effects, and contraindications."
    response = model.generate_content(prompt)
    return response.text

# Function to check symptoms and recommend potential drugs
def symptom_checker(symptoms):
    prompt = f"Given these symptoms: {symptoms}, suggest possible over-the-counter medications and include any relevant side-effect information. This is for educational purposes only."
    response = model.generate_content(prompt)
    return response.text

# Example usage
drug_name = "Ibuprofen"
symptoms = "headache, mild fever"

print("Drug Information:")
print(get_drug_information(drug_name))

print("\nSymptom Checker:")
print(symptom_checker(symptoms))
