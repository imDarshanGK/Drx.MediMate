import google.generativeai as genai

# Configure API key for Gemini
genai.configure(api_key="AIzaSyCbx-")
model = genai.GenerativeModel("gemini-1.5-flash-8b")

def cyber_attack_response(query):
    prompt = f"You are a cybersecurity expert. Explain about {query}. If it's an ongoing attack, suggest real-time mitigation steps."
    response = model.generate_content(prompt)
    return response.text if response else "I couldn't process your request."

query = "What is a sql injection"
print(cyber_attack_response(query))
