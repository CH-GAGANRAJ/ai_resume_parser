# Resume Parser Application

A complete solution for parsing resumes, extracting key information, and storing them in a database with analysis capabilities.

## Features

- **Resume Processing**: Supports PDF, DOCX, DOC, and TXT formats
- **Information Extraction**: Extracts name, email, phone, skills, experience
- **AI Analysis**: Provides resume rating, improvement areas, and upskill suggestions
- **Database Storage**: Saves all parsed resumes for future reference
- **User Interface**: Simple Streamlit dashboard for uploading and viewing resumes

## Project Structure
```bash
resume-parser/
├── interface.py          # Streamlit user interface
├── main.py               # FastAPI backend server
├── database.py           # Database connection and setup
├── models.py             # Database models
├── crud.py               # Database operations
├── resume_parser.py      # Resume parsing logic
├── utils.py              # File conversion utilities
├── requirements.txt      # Python dependencies
└── README.md
```
## Running the Application

- **Backend Server (FastAPI)**
- **Start the FastAPI server:**
```bash
uvicorn main:app --reload
```
The API will be available at http://localhost:8000
- **Frontend Interface (Streamlit)**
- **Start the Streamlit interface:**
```bash
streamlit run interface.py
```
## Usage
# Upload New Resume:
- **Go to the "Upload New Resume" tab**
- **Select a resume file (PDF, DOCX, DOC, or TXT)**
- **Click "Upload and Parse"**
- **View the extracted information**
# View Past Resumes:
- **Go to the "View Past Resumes" tab**
- **See all previously uploaded resumes in a table**
- **Select a resume from the dropdown to view detailed information**
## Screenshots
