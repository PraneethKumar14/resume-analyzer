# Resume Analyzer

![Resume Analyzer](https://img.shields.io/badge/Python-3.8%2B-blue) ![React](https://img.shields.io/badge/React-18%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)

A powerful web application that analyzes resumes for ATS (Applicant Tracking System) compatibility, provides actionable feedback, and displays the resume with live highlighting of issues.

## Features

✅ **File Upload**: Upload PDF or DOCX resumes (max 5MB)  
✅ **PDF Rendering**: View your actual PDF resume in the browser using PDF.js  
✅ **ATS Analysis**: Comprehensive analysis against industry keywords and best practices  
✅ **Job Description Matching**: Get targeted suggestions based on specific job requirements  
✅ **Live Feedback**: Color-coded issues with actionable suggestions  
✅ **Professional UI**: Modern, responsive design with gradient styling  
✅ **Multiple Issue Types**: Critical, medium, and low priority issues  

## Screenshots

### Upload Interface
![Upload Interface](https://via.placeholder.com/800x400/667eea/ffffff?text=Upload+Resume+Interface)

### Analysis Results
![Analysis Results](https://via.placeholder.com/800x400/764ba2/ffffff?text=ATS+Analysis+Results)

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction
- **pdfminer.six** - Advanced PDF parsing

### Frontend
- **React 18** - JavaScript library
- **PDF.js** - PDF rendering
- **Axios** - HTTP client
- **CSS3** - Styling with gradients and responsive design

## Installation

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)
- [Git](https://git-scm.com/)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

## Usage

### Running the Application

You need **two terminal windows** to run both backend and frontend simultaneously.

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Access the Application

- **Backend API**: `http://localhost:5001`
- **Frontend Interface**: `http://localhost:3000` (opens automatically)

### Using the Application

1. **Upload Resume**: Click "Choose File" and select your PDF or DOCX resume
2. **Optional**: Paste a job description for targeted suggestions
3. **Analyze**: Click "Analyze Resume" to get ATS feedback
4. **Review Results**: 
   - View your resume in the left panel
   - See color-coded issues in the right panel
   - Get actionable suggestions for improvement
5. **Upload New**: Click "Upload New Resume" to analyze another file

## API Endpoints

### Backend Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint |
| `/upload` | POST | Upload and analyze resume |
| `/uploads/<filename>` | GET | Serve uploaded files |

### Upload Request Format

**Form Data:**
- `file`: Resume file (PDF/DOCX, max 5MB)
- `job_description`: Optional job description text

### Response Format

```json
{
  "success": true,
  "filename": "resume.pdf",
  "file_type": "pdf",
  "resume_text": "First 500 characters of resume...",
  "issues": [
    {
      "type": "missing_keywords",
      "message": "Missing keywords: python, aws",
      "severity": "high",
      "suggestion": "Add these keywords to your skills section"
    }
  ]
}
```

## Analysis Features

### Keyword Detection
- **Technical Skills**: 100+ programming languages, frameworks, and tools
- **Action Verbs**: Strong verbs for impactful resume writing
- **Weak Phrases**: Identifies passive language to avoid

### Content Analysis
- **Section Completeness**: Checks for essential resume sections
- **Quantifiable Achievements**: Detects measurable results
- **Contact Information**: Verifies presence of contact details
- **Resume Length**: Validates optimal word count

### Job Description Matching
When a job description is provided, the analyzer:
- Extracts relevant keywords from the job posting
- Compares against your resume content
- Highlights missing job-specific requirements

## Issue Severity Levels

| Severity | Color | Description |
|----------|-------|-------------|
| **High** | 🚨 Red | Critical issues that significantly impact ATS scoring |
| **Medium** | ⚠️ Yellow | Important improvements for better compatibility |
| **Low** | ℹ️ Blue | Minor suggestions for optimization |

## Development

### Project Structure
```
resume-analyzer/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── utils/              # Analysis utilities
│       ├── pdf_parser.py
│       ├── docx_parser.py
│       └── ats_analyzer.py
├── frontend/
│   ├── public/             # Static files
│   └── src/                # React components
│       ├── App.js
│       ├── App.css
│       └── components/
│           └── PDFViewer.js
└── README.md
```

### Environment Variables
The application uses default configuration. To customize:

- **UPLOAD_FOLDER**: Change upload directory
- **MAX_FILE_SIZE**: Adjust file size limit
- **Port**: Modify Flask port in `app.py`

## Deployment

### Local Development
Follow the usage instructions above for local development.

### Production Deployment
- **Backend**: Deploy to Render, Heroku, or PythonAnywhere
- **Frontend**: Deploy to Netlify, Vercel, or GitHub Pages

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PDF.js](https://mozilla.github.io/pdf.js/) - PDF rendering library
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [React](https://reactjs.org/) - JavaScript UI library

## Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Contact: your-email@example.com

---

**Made with ❤️ for job seekers everywhere!**

*Optimize your resume. Land your dream job.*