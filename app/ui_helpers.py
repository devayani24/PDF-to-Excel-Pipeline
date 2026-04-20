from tkinter import filedialog
import pdfplumber

def select_pdf_file():
    return filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

def select_save_location(default_name="output.csv"):
    return filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialfile=default_name,
        filetypes=[("CSV Files", "*.csv")]
    )

def is_pdf_encrypted(filepath):
    try:
        with pdfplumber.open(filepath) as pdf:
            pdf.pages[0].extract_text()
            return False
    except Exception as e:
        return True