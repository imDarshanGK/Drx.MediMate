
from flask import Blueprint, render_template, request, jsonify
from backend.utils.gemini_utils import (
    get_drug_information,
    get_symptom_recommendation,
    analyze_image_with_gemini,
    analyze_prescription_with_gemini
)

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ask", methods=["POST"])
def ask_gemini():
    data = request.json
    question_type = data.get("type")

    if question_type == "drug":
        response = get_drug_information(data.get("query", ""))
    elif question_type == "symptom":
        response = get_symptom_recommendation(data.get("query", ""))
    else:
        response = "Unknown query type."

    return jsonify({"response": response})


@ai_bp.route("/upload-image", methods=["POST"])
def upload_image():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = image.read()
    try:
        result = analyze_image_with_gemini(image_bytes)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/validate-prescription', methods=['POST'])
def validate_prescription():
    logging.info("📩 API /validate-prescription called")

    image_data = request.form.get("image_data")
    if image_data:
        logging.info("📷 Prescription image data received for validation")

        # Process the image with Gemini (replace with your validator logic)
        result = analyze_prescription_with_gemini(image_data)

        logging.info(f"✅ Gemini result: {result}")
        return jsonify({'result': result})
    else:
        logging.warning("❌ No image data received in /validate-prescription")
        return jsonify({'result': '❌ No image received for validation.'})

