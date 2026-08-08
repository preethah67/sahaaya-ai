import os
import uuid
from flask import Flask, render_template, request, jsonify
from ai_pipeline import analyze_document
from voice_engine import text_to_speech

app = Flask(__name__)

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
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    ai_result = analyze_document(text_content=user_text)

    audio_filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
    text_to_speech(ai_result.get('tanglish_summary', ''), audio_filename, lang='en')

    return jsonify({
        'status': 'success',
        'data': ai_result,
        'audio_url': f"/static/audio/{audio_filename}"
    })

@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f"doc_{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Directly analyze image with Gemini Vision (Ultra-low RAM usage)
    ai_result = analyze_document(image_path=file_path)

    audio_filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
    text_to_speech(ai_result.get('tanglish_summary', ''), audio_filename, lang='en')

    # Clean up uploaded image file to save disk space
    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify({
        'status': 'success',
        'data': ai_result,
        'audio_url': f"/static/audio/{audio_filename}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)