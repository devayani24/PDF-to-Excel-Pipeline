import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import os
from datetime import datetime
import pdfplumber

from app.ui_helpers import select_pdf_file, select_save_location, is_pdf_encrypted

from src.processors.indian_bank_processor import IndianBankProcessor
from src.processors.kotak_processor import KotakProcessor
from src.processors.canara_bank_processor import CanaraBankProcessor
from src.processors.city_union_bank_processor import CityUnionBankProcessor
from src.processors.HDFC_processor import HDFCProcessor
from src.processors.KVB_processor import KVBProcessor
from src.processors.SBI_processor import SBIProcessor


# ---------------- STATE ---------------- #
selected_file = None
selected_bank = None

BANK_PROCESSORS = {
    "Indian Bank": IndianBankProcessor,
    "Kotak": KotakProcessor,
    "Canara Bank": CanaraBankProcessor,
    "City Union Bank": CityUnionBankProcessor,
    "HDFC": HDFCProcessor,
    "KVB": KVBProcessor,
    "SBI": SBIProcessor
}


# ---------------- CORE LOGIC ---------------- #

def upload_file():
    global selected_file

    filepath = select_pdf_file()
    if not filepath:
        return

    selected_file = filepath
    file_label.config(text=os.path.basename(filepath))
    file_frame.pack(pady=5)

    upload_btn.config(state="disabled")
    check_ready()


def remove_file():
    global selected_file

    selected_file = None
    file_frame.pack_forget()

    delete_btn.config(state="disabled")
    process_btn.config(state="disabled")

    if selected_bank:
        upload_btn.config(state="normal")


def on_bank_select(event):
    global selected_bank

    selection = bank_listbox.curselection()
    if selection:
        selected_bank = bank_listbox.get(selection[0])
        upload_btn.config(state="normal")
        check_ready()


def check_ready():
    if selected_bank and selected_file:
        process_btn.config(state="normal")


# ---------------- PROCESSING ---------------- #

def process_file():
    if not selected_file:
        messagebox.showerror("Error", "Please upload a PDF")
        return

    password = handle_pdf_password()

    # STOP if user cancelled
    if password is None and is_pdf_encrypted(selected_file):
        return

    loading_label.pack(pady=10)
    disable_ui()

    threading.Thread(target=run_process, args=(password,)).start()


def handle_pdf_password():
    if not is_pdf_encrypted(selected_file):
        return None

    while True:
        password = simpledialog.askstring(
            "Password Required",
            "Enter PDF password:",
            show="*",
            parent=root
        )

        if password is None:
            return


        try:
            with pdfplumber.open(selected_file, password=password) as pdf:
                _ = pdf.pages[0].extract_text()
            return password

        except Exception:
            messagebox.showerror("Error", "Incorrect password. Try again.")


def run_process(password):
    try:
        processor_class = BANK_PROCESSORS.get(selected_bank)

        if not processor_class:
            raise ValueError("Unsupported bank")

        processor = processor_class(selected_file, password)
        df = processor.transform()

        save_file(df)

    except Exception as e:
        root.after(0, lambda err=e: messagebox.showerror("Error", str(err)))

    finally:
        root.after(0, finish_processing)


def save_file(df):
    base_name = os.path.splitext(os.path.basename(selected_file))[0]
    timestamp = datetime.now().strftime("%d%m%y_%H%M")

    filename = f"{base_name}_output_{timestamp}.csv"
    path = select_save_location(filename)

    if path:
        df.to_csv(path, index=False)
        root.after(0, lambda: messagebox.showinfo("Success", f"Saved at:\n{path}"))


# ---------------- UI STATE ---------------- #

def disable_ui():
    upload_btn.config(state="disabled")
    process_btn.config(state="disabled")
    clear_btn.config(state="disabled")
    bank_listbox.config(state="disabled")
    delete_btn.config(state="disabled")

    root.config(cursor="watch")   # loading cursor


def enable_ui():
    bank_listbox.config(state="normal")
    clear_btn.config(state="normal")

    # Upload button
    if selected_bank:
        upload_btn.config(state="normal")
    else:
        upload_btn.config(state="disabled")

    # File display
    if selected_file:
        file_frame.pack(pady=5)
        delete_btn.config(state="normal")
    else:
        file_frame.pack_forget()
        delete_btn.config(state="disabled")

    # Process button
    if selected_bank and selected_file:
        process_btn.config(state="normal")
    else:
        process_btn.config(state="disabled")

    root.config(cursor="")


def finish_processing():
    loading_label.pack_forget()
    enable_ui()


def clear_all():
    global selected_file, selected_bank

    selected_file = None
    selected_bank = None

    bank_listbox.selection_clear(0, tk.END)
    file_frame.pack_forget()

    upload_btn.config(state="disabled")
    process_btn.config(state="disabled")
    delete_btn.config(state="disabled")


# ---------------- UI ---------------- #

root = tk.Tk()
root.title("PDF to Excel Tool")

root.state("zoomed")          # full screen
root.minsize(900, 600)        # prevent too small window
root.configure(bg="#f4f6f9")

main_frame = tk.Frame(root, bg="#ffffff", padx=60, pady=60)
main_frame.pack(expand=True, fill="both", padx=200, pady=70)

# Company Name
company_label = tk.Label(
    main_frame,
    text="DEEJAY INFOTECH",
    font=("Segoe UI", 12, "bold"),
    fg="#cc0000",          # subtle brand color
    bg="#ffffff"
)
company_label.pack(pady=(0, 2))

# Title
title_label = tk.Label(
    main_frame,
    text="PDF to Excel Converter",
    font=("Segoe UI", 22, "bold"),
    fg="#1f4e79",
    bg="#ffffff"
)
title_label.pack(pady=(5, 25))


# Bank selection
tk.Label(main_frame, text="Select Bank", bg="#ffffff").pack()

bank_listbox = tk.Listbox(
    main_frame,
    height=8,
    width=40,
    font=("Segoe UI", 10),
    selectbackground="#4a90e2"
)

for bank in BANK_PROCESSORS.keys():
    bank_listbox.insert(tk.END, bank)

bank_listbox.pack(pady=10)
bank_listbox.bind("<<ListboxSelect>>", on_bank_select)


# Upload button
upload_btn = tk.Button(
    main_frame,
    text="Upload PDF",
    width=22,
    command=upload_file,
    state="disabled",
    bg="#4a90e2",
    fg="white",
    font=("Segoe UI", 11)
)
upload_btn.pack(pady=10)


# File display
file_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=10, pady=5)

file_label = tk.Label(file_frame, bg="#f0f0f0")
file_label.pack(side="left")

delete_btn = tk.Button(
    file_frame,
    text="✖",
    command=remove_file,
    bg="#f0f0f0",
    bd=0
)
delete_btn.pack(side="right")


# Process button
process_btn = tk.Button(
    main_frame,
    text="Process",
    width=22,
    command=process_file,
    state="disabled",
    bg="#27ae60",
    fg="white",
    font=("Segoe UI", 11)
)
process_btn.pack(pady=10)


# Clear button
clear_btn = tk.Button(
    main_frame,
    text="Clear",
    width=22,
    command=clear_all,
    font=("Segoe UI", 11)
)
clear_btn.pack(pady=5)


# Loading label
loading_label = tk.Label(
    main_frame,
    text="Processing...",
    fg="orange",
    bg="#ffffff"
)


root.mainloop()