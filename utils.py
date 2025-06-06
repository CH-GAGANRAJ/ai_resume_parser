import os
import fitz # PyMuPDF
import docx2txt
import warnings
import textract

warnings.filterwarnings("ignore", category=UserWarning)

# function to convert pdf to text
def pdf_to_text(file_path):
    text=""
    try:
        doc=fitz.open(file_path)
        for page in doc:
            text+=page.get_text()
        doc.close()
    except Exception as e:
        pass
    return text

# Function to convert docx to text
def docx_to_text(file_path):
    text=""
    try:
        doc=docx2txt.process(file_path)
        text+=doc
    except Exception as e:
        pass
    return text

# Function to covert doc to text
def doc_to_text(file_path):
    text=""
    try:
        text=textract.process(file_path).decode('utf-8',errors='ignore')
    except Exception as e:
        pass
    return text

# To covert resumes to text from any format to text and returns it
def convert_resume_to_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    text_content = ""

    if file_extension == ".pdf":
        try:
            # Calling function to covert pdf to text
            text_content = pdf_to_text(file_path)
        except Exception as e:
            print(f"Caught exception during PDF conversion for {file_path}: {e}")
    elif file_extension == ".docx":
        # calling function to convert docx to text
        text_content = docx_to_text(file_path)
    elif file_extension == ".doc":
        # calling function to convert docx to text
        text_content = doc_to_text(file_path)
    elif file_extension == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text_content = f.read()
    # else:
        # print(f"Unsupported file format: {file_extension}")

    return text_content