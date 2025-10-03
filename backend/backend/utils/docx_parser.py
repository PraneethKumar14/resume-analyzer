from docx import Document
import io

def extract_text_from_docx(file_stream):
    try:
        file_stream.seek(0)
        doc = Document(file_stream)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return ""