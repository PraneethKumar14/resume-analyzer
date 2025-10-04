import io
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def extract_text_from_pdf(file_stream):
    """Extract text from PDF using multiple methods with better error handling"""
    try:
        # Method 1: Try pdfminer first (most accurate)
        file_stream.seek(0)
        text = pdfminer_extract_text(file_stream)
        
        # If pdfminer returns empty or very short text, try alternative method
        if not text or len(text.strip()) < 50:
            file_stream.seek(0)
            text = extract_text_with_pdfminer_detailed(file_stream)
        
        # Clean up the text
        cleaned_text = clean_extracted_text(text)
        print(f"✅ Successfully extracted {len(cleaned_text)} characters from PDF")
        return cleaned_text
        
    except Exception as e:
        print(f"❌ Error extracting PDF text: {e}")
        # Fallback to basic extraction
        try:
            file_stream.seek(0)
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(file_stream)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            cleaned_text = clean_extracted_text(text)
            print(f"✅ Fallback extraction successful: {len(cleaned_text)} characters")
            return cleaned_text
        except Exception as e2:
            print(f"❌ All extraction methods failed: {e2}")
            return "ERROR: Could not extract text from PDF"

def extract_text_with_pdfminer_detailed(file_stream):
    """Alternative pdfminer extraction method"""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    file_stream.seek(0)
    for page in PDFPage.get_pages(file_stream, caching=True, check_extractable=True):
        page_interpreter.process_page(page)
    
    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def clean_extracted_text(text):
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:  # Only keep non-empty lines
            cleaned_lines.append(stripped)
    
    return '\n'.join(cleaned_lines)

def get_pdf_page_count(file_stream):
    """Get number of pages in PDF"""
    try:
        import PyPDF2
        file_stream.seek(0)
        pdf_reader = PyPDF2.PdfReader(file_stream)
        return len(pdf_reader.pages)
    except:
        return 1