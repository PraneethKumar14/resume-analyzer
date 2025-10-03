import io
from pdfminer.high_level import extract_text as pdfminer_extract_text

def extract_text_from_pdf(file_stream):
    try:
        file_stream.seek(0)
        text = pdfminer_extract_text(file_stream)
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def get_pdf_page_count(file_stream):
    try:
        import PyPDF2
        file_stream.seek(0)
        pdf_reader = PyPDF2.PdfReader(file_stream)
        return len(pdf_reader.pages)
    except:
        return 1