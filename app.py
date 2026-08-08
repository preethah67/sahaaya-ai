import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from ai_pipeline import analyze_document_text
from ocr_engine import extract_text_from_image
from voice_engine import text_to_speech

app = Flask(__name__)

# Configure upload and audio directories
UPLOAD_FOLDER = os.path.join('static', 'uploads')
AUDIO_FOLDER = os.path.join('static', 'audio')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-text', methods=['POST'])
def process_text():
    """Processes plain text or transcript from Speech-to-Text."""
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    # 1. Run AI analysis
    ai_result = analyze_document_text(user_text)

    # 2. Generate Voice MP3 for Tanglish summary
    audio_filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
    text_to_speech(ai_result.get('tanglish_summary', ''), audio_filename, lang='en')

    return jsonify({
        'status': 'success',
        'data': ai_result,
        'audio_url': f"/static/audio/{audio_filename}"
    })

@app.route('/upload-document', methods=['POST'])
def upload_document():
    """Handles image upload, performs OCR, and passes text to AI pipeline."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded image
    filename = f"doc_{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # 1. Perform OCR
    extracted_text = extract_text_from_image(file_path)

    if not extracted_text:
        return jsonify({'error': 'Could not extract text from the document image.'}), 400

    # 2. Run AI Analysis on extracted OCR text
    ai_result = analyze_document_text(extracted_text)

    # 3. Generate Voice MP3 for Tanglish summary
    audio_filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
    text_to_speech(ai_result.get('tanglish_summary', ''), audio_filename, lang='en')

    return jsonify({
        'status': 'success',
        'extracted_text': extracted_text,
        'data': ai_result,
        'audio_url': f"/static/audio/{audio_filename}"
    })

if __name__ == '__main__':
    print("🚀 Sahaaya AI Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)