# PDF to Excel Converter (Finance Data Pipeline)

A production-grade Python application that converts bank statement PDFs into structured Excel files.  
Designed to handle multiple bank formats with a scalable and modular architecture.

---

## Features

- ✅ Convert PDF bank statements to Excel
- ✅ Supports multiple banks (Indian Bank, Canara, Kotak, City Union Bank, etc.)
- ✅ Handles encrypted/password-protected PDFs
- ✅ Intelligent transaction parsing (date, debit, credit, balance)
- ✅ Clean and structured Excel output
- ✅ User-friendly Tkinter GUI
- ✅ Extensible architecture for adding new banks

## Installation

### 1. Clone the repository

git clone https://github.com/devayani24/PDF-to-Excel-Pipeline.git
cd pdf-to-excel-pipeline

### 2. Virtual environment
#### 1. Create virtual environment
python -m venv venv

#### 2. Activate environment
venv\Scripts\activate   # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
python app/ui.py
Steps:
- Select a bank
- Upload PDF file
- Enter password (if required)
- Choose save location
- Click Process

✅ Output will be saved as Excel file

## Handling Encrypted PDFs

The application automatically:

Detects if PDF is password protected
Prompts user for password
Retries if incorrect password is entered

## Architecture

This project follows a modular + scalable design:

Processor Layer → Handles orchestration
Parser Layer → Extracts and structures transactions
Bank-specific classes → Custom logic per bank
UI Layer → User interaction

## Easy to extend:

To add a new bank:

Create a new processor in src/processors/
Override parsing logic if needed
Plug into UI

## Tech Stack
- Python
- Pandas
- PDFPlumber
- PyMuPDF (fitz)
- Tkinter
- Regex

## Future Improvements
- XML export support
- Cloud deployment (AWS)
- API-based processing (FastAPI)
- Drag-and-drop UI
- Auto bank detection

## Known Limitations
Highly inconsistent PDF formats may require custom parsing

## Author

Devayani Senthilvelan

Data Science & Backend Engineering
Python | ML | NLP | Computer Vision
