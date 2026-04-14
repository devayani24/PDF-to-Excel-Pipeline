# PDF to Excel Converter (Finance Data Pipeline)

A production-grade Python application that converts bank statement PDFs into structured Excel files.  
Designed to handle multiple bank formats with a scalable and modular architecture.

---

## Features

- ✅ Convert PDF bank statements to Excel
- ✅ Supports multiple banks (Indian Bank, Canara, Kotak, City Union Bank, etc.)
- ✅ Handles encrypted/password-protected PDFs
- ✅ OCR support for scanned PDFs (Tesseract)
- ✅ Intelligent transaction parsing (date, debit, credit, balance)
- ✅ Clean and structured Excel output
- ✅ User-friendly Tkinter GUI
- ✅ Extensible architecture for adding new banks

---

## Project Structure
PDF-to-Excel-Pipeline/
│
├── app/
│ └── ui.py # Tkinter UI
│
├── src/
│ ├── components/ # Core logic
│ │ ├── ingestion.py
│ │ ├── transaction_parser.py
│ │
│ ├── processors/ # Bank-specific processors
│ │ ├── indian_bank_processor.py
│ │ ├── kotak_processor.py
│ │ ├── canara_bank_processor.py
│ │
│ ├── utils.py # Helper functions
│ ├── exception.py
│ └── logger.py
│
├── data/ # Sample PDFs (ignored in git)
├── output/ # Generated Excel files
├── requirements.txt
└── README.md


---

## Installation

### 1. Clone the repository

git clone https://github.com/your-username/pdf-to-excel-pipeline.git
cd pdf-to-excel-pipeline

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
python app/ui.py
Steps:
Select a bank
Upload PDF file
Enter password (if required)
Choose save location
Click Process

✅ Output will be saved as Excel file

## Handling Encrypted PDFs

The application automatically:

Detects if PDF is password protected
Prompts user for password
Retries if incorrect password is entered

🧠 Architecture

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
Python
Pandas
PDFPlumber
PyMuPDF (fitz)
Tesseract OCR
Tkinter
Regex

## Future Improvements
XML export support
Cloud deployment (AWS)
API-based processing (FastAPI)
Drag-and-drop UI
Auto bank detection
Improved OCR accuracy

## Known Limitations
Highly inconsistent PDF formats may require custom parsing

## Author

Devayani Senthilvelan

Data Science & Backend Engineering
Python | ML | NLP | Computer Vision
