from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed.'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read file content
        file.seek(0)
        if filename.lower().endswith('.pdf'):
            from utils.pdf_parser import extract_text_from_pdf
            resume_text = extract_text_from_pdf(file)
            file_type = 'pdf'
        else:
            from utils.docx_parser import extract_text_from_docx
            resume_text = extract_text_from_docx(file)
            file_type = 'docx'
        
        # Get job description if provided
        job_description = request.form.get('job_description', '')
        
        # Analyze with job description support
        from utils.ats_analyzer import analyze_resume_text
        issues = analyze_resume_text(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_type': file_type,
            'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text,
            'issues': issues
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

# Add this route to serve uploaded files (CRUCIAL for PDF display)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("🚀 Resume Analyzer Backend Starting...")
    print("📍 Running on http://localhost:5001")
    print("✅ Health check: http://localhost:5001/health")
    print("📤 Upload endpoint: http://localhost:5001/upload")
    print("📂 File serving: http://localhost:5001/uploads/<filename>")
    app.run(debug=True, port=5001)