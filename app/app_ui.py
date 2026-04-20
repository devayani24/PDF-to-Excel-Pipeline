import sys
sys.path.insert(0, ".")

import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import os
from datetime import datetime
import pdfplumber

from ui_helpers import select_pdf_file, select_save_location, is_pdf_encrypted

from src.processors.indian_bank_processor import IndianBankProcessor
from src.processors.kotak_processor import KotakProcessor
from src.processors.canara_bank_processor import CanaraBankProcessor
from src.processors.city_union_bank_processor import CityUnionProcessor
from src.processors.HDFC_processor import HDFCProcessor
from src.processors.KVB_processor import KVBProcessor
from src.processors.SBI_processor import SBIProcessor
from src.logger import logging

# ─── COLORS ───────────────────────────────────────────────────────────────────
BG          = "#F0F2F5"
CARD_BG     = "#FFFFFF"
PRIMARY     = "#1A3C6E"       # deep navy
ACCENT      = "#2E7DF7"       # bright blue
SUCCESS     = "#16A34A"       # green
DANGER      = "#DC2626"       # red
MUTED       = "#6B7280"       # gray text
BORDER      = "#E5E7EB"
STEP_ACTIVE = "#2E7DF7"
STEP_DONE   = "#16A34A"
STEP_IDLE   = "#D1D5DB"
TEXT_DARK   = "#111827"
TEXT_MID    = "#374151"
HOVER_BLUE  = "#1D6FE8"
HOVER_GREEN = "#15803D"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_SUB    = ("Segoe UI", 10)
FONT_LABEL  = ("Segoe UI", 9, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 8)
FONT_STEP   = ("Segoe UI", 8, "bold")
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_STATUS = ("Segoe UI", 9)

# ─── STATE ────────────────────────────────────────────────────────────────────
selected_file = None
selected_bank = None

BANK_PROCESSORS = {
    "Indian Bank":    IndianBankProcessor,
    "Kotak":          KotakProcessor,
    "Canara Bank":    CanaraBankProcessor,
    "City Union Bank":CityUnionProcessor,
    "HDFC":           HDFCProcessor,
    "KVB":            KVBProcessor,
    "SBI":            SBIProcessor,
}

BANK_LIST = list(BANK_PROCESSORS.keys())

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kwargs)
    canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0,   extent=90,  style="pieslice", **kwargs)
    canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90,  style="pieslice", **kwargs)
    canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90,  style="pieslice", **kwargs)
    canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs)
    canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs)


def make_button(parent, text, command, bg, fg="white", width=200, height=38):
    frame = tk.Frame(parent, bg=parent["bg"] if hasattr(parent, "__getitem__") else BG)
    canvas = tk.Canvas(frame, width=width, height=height,
                       bg=parent.cget("bg"), highlightthickness=0)
    canvas.pack()

    def draw(color):
        canvas.delete("all")
        rounded_rect(canvas, 1, 1, width-1, height-1, 8,
                     fill=color, outline=color)
        canvas.create_text(width//2, height//2, text=text,
                           font=FONT_BTN, fill=fg)

    draw(bg)

    hover_color = HOVER_BLUE if bg == ACCENT else (HOVER_GREEN if bg == SUCCESS else "#9CA3AF")

    canvas.bind("<Enter>",  lambda e: draw(hover_color))
    canvas.bind("<Leave>",  lambda e: draw(bg))
    canvas.bind("<Button-1>", lambda e: command())

    frame._canvas = canvas
    frame._bg     = bg
    frame._draw   = draw

    return frame


# ─── STEP INDICATOR ───────────────────────────────────────────────────────────
def update_steps(step):
    """step: 1, 2, or 3"""
    for i, (circle, label) in enumerate(zip(step_circles, step_labels), 1):
        if i < step:
            color = STEP_DONE
            symbol = "✓"
        elif i == step:
            color = STEP_ACTIVE
            symbol = str(i)
        else:
            color = STEP_IDLE
            symbol = str(i)

        circle.delete("all")
        circle.create_oval(2, 2, 26, 26, fill=color, outline=color)
        circle.create_text(14, 14, text=symbol,
                           font=FONT_STEP, fill="white")
        label.config(fg=color if i <= step else MUTED)


# ─── BANK SELECTION ───────────────────────────────────────────────────────────
bank_buttons = {}

def on_bank_select(bank):
    global selected_bank, selected_file
    selected_bank = bank

    # If a file was already loaded — remove it
    if selected_file:
        selected_file = None
        file_display_frame.grid_remove()
        process_btn_frame.grid_remove()
        status_var.set(f"Bank changed to {bank}. Please re-upload your PDF.")
    else:
        status_var.set(f"Bank selected: {bank}. Now upload your PDF.")

    for b, (btn_frame, indicator) in bank_buttons.items():
        if b == bank:
            indicator.config(bg=ACCENT)
            btn_frame.config(bg="#EFF6FF", highlightbackground=ACCENT)
        else:
            indicator.config(bg=BORDER)
            btn_frame.config(bg=CARD_BG, highlightbackground=BORDER)

    upload_btn_frame.grid()
    update_steps(2)
    check_ready()


# ─── FILE HANDLING ────────────────────────────────────────────────────────────
def upload_file():
    global selected_file
    filepath = select_pdf_file()
    if not filepath:
        return

    selected_file = filepath
    fname = os.path.basename(filepath)
    short = fname if len(fname) <= 35 else fname[:32] + "..."

    file_name_label.config(text=short)
    file_display_frame.grid()
    status_var.set(f"File loaded: {fname}. Click Process to continue.")
    update_steps(3)
    check_ready()


def remove_file():
    global selected_file
    selected_file = None
    file_display_frame.grid_remove()
    process_btn_frame.grid_remove()
    status_var.set("File removed. Please upload a PDF.")
    update_steps(2)


def check_ready():
    if selected_bank and selected_file:
        process_btn_frame.grid()
    else:
        process_btn_frame.grid_remove()


# ─── PROCESSING ───────────────────────────────────────────────────────────────
def process_file():
    if not selected_file:
        messagebox.showerror("Error", "Please upload a PDF")
        return

    password = handle_pdf_password()
    if password is None and is_pdf_encrypted(selected_file):
        return

    show_loading(True)
    threading.Thread(target=run_process, args=(password,), daemon=True).start()


def handle_pdf_password():
    if not is_pdf_encrypted(selected_file):
        return None
    while True:
        password = simpledialog.askstring(
            "Password Required",
            "This PDF is password protected.\nEnter password:",
            show="*", parent=root
        )
        if password is None:
            return None
        try:
            with pdfplumber.open(selected_file, password=password) as pdf:
                pdf.pages[0].extract_text()
            return password
        except Exception:
            messagebox.showerror("Wrong Password", "Incorrect password. Please try again.")

def validate_output(df) -> tuple[bool, str]:
    """
    Returns (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, (
            "No transactions were extracted from this PDF.\n\n"
            "Please check:\n"
            "  • Correct bank is selected\n"
            "  • PDF contains transaction data\n"
            "  • PDF is not a scanned image"
        )

    if len(df) <= 1:
        return False, (
            f"Only {len(df)} row was extracted — no transaction data found.\n\n"
            "Please check:\n"
            "  • Correct bank is selected\n"
            "  • PDF contains transaction data\n"
            "  • PDF is not a scanned image"
        )

    lengths  = {col: len(df[col]) for col in df.columns}
    all_same = len(set(lengths.values())) == 1

    if not all_same:
        return False, (
            f"Extracted data has inconsistent columns.\n\n"
            f"{lengths}\n\n"
            "Please contact support."
        )

    return True, ""

def run_process(password):
    try:
        processor_class = BANK_PROCESSORS.get(selected_bank)
        if not processor_class:
            raise ValueError("Unsupported bank selected")

        root.after(0, lambda: status_var.set("Processing... please wait"))
        processor = processor_class(selected_file, password)
        df        = processor.transform()

        is_valid, error_msg = validate_output(df)
        if not is_valid:
            root.after(0, lambda msg=error_msg: messagebox.showerror("Validation Failed", msg))
            return

        save_file(df)

    except Exception as e:
        logging.error(f"Processing failed: {e}")
        root.after(0, lambda: messagebox.showerror(
            "Processing Failed",
            f"Could not process {selected_bank} PDF.\n\n"
            f"Please check:\n"
            f"  • Correct bank is selected\n"
            f"  • PDF is not corrupted\n"
            f"  • Password is correct (if encrypted)\n\n"
            f"Contact support if issue persists."
        ))
    finally:
        root.after(0, lambda: show_loading(False))


def save_file(df):
    base_name = os.path.splitext(os.path.basename(selected_file))[0]
    timestamp = datetime.now().strftime("%d%m%y_%H%M")
    filename  = f"{base_name}_output_{timestamp}.csv"
    path      = select_save_location(filename)

    if path:
        df.to_csv(path, index=False)
        root.after(0, lambda: [
            status_var.set(f"✓ Saved successfully — {len(df)} transactions extracted"),
            messagebox.showinfo(
                "Success",
                f"✅  Processing complete!\n\n"
                f"Transactions extracted : {len(df)}\n"
                f"Saved at               : {path}"
            )
        ])
    else:
        root.after(0, lambda: [
            status_var.set("Save cancelled."),
            messagebox.showwarning("Cancelled", "File was not saved.")
        ])


# ─── UI STATE ─────────────────────────────────────────────────────────────────
def show_loading(state: bool):
    if state:
        loading_frame.grid()
        process_btn_frame.grid_remove()
        status_var.set("Processing... please wait")
        root.config(cursor="watch")

        # Freeze bank buttons
        for b, (btn_frame, indicator) in bank_buttons.items():
            btn_frame.unbind("<Button-1>")
            for child in btn_frame.winfo_children():
                child.unbind("<Button-1>")

        # Freeze upload button
        if hasattr(upload_btn_frame, '_canvas'):
            upload_btn_frame._canvas.unbind("<Button-1>")
            upload_btn_frame._canvas.unbind("<Enter>")
            upload_btn_frame._canvas.unbind("<Leave>")

        # Freeze remove button ← key fix
        for widget in file_display_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled", command=lambda: None)

    else:
        loading_frame.grid_remove()
        if selected_bank and selected_file:
            process_btn_frame.grid()
        root.config(cursor="")

        # Restore bank buttons
        for b, (btn_frame, indicator) in bank_buttons.items():
            btn_frame.bind("<Button-1>", lambda e, bk=b: on_bank_select(bk))
            for child in btn_frame.winfo_children():
                child.bind("<Button-1>", lambda e, bk=b: on_bank_select(bk))

        # Restore upload button
        if hasattr(upload_btn_frame, '_canvas'):
            upload_btn_frame._canvas.bind("<Button-1>", lambda e: upload_file())
            upload_btn_frame._canvas.bind("<Enter>",  lambda e: upload_btn_frame._draw(HOVER_BLUE))
            upload_btn_frame._canvas.bind("<Leave>",  lambda e: upload_btn_frame._draw(ACCENT))

        # Restore remove button ← key fix
        for widget in file_display_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="normal", command=remove_file)


def clear_all():
    global selected_file, selected_bank
    selected_file = None
    selected_bank = None

    for b, (btn_frame, indicator) in bank_buttons.items():
        indicator.config(bg=BORDER)
        btn_frame.config(bg=CARD_BG, highlightbackground=BORDER)

    file_display_frame.grid_remove()
    process_btn_frame.grid_remove()
    upload_btn_frame.grid_remove()
    status_var.set("Select a bank to get started.")
    update_steps(1)


# ─── BUILD UI ─────────────────────────────────────────────────────────────────
import sys
import os
import ctypes

def resource_path(relative_path):
    """Get absolute path — works for both dev and PyInstaller exe"""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


root = tk.Tk()

root.iconbitmap(resource_path("bankstatement_pro.ico"))

# Force Windows to use correct icon
ico_path = resource_path("bankstatement_pro.ico")
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "DeeJayInfotech.BankStatementPro.2.0.0"
)

# This is the key fix for taskbar
root.wm_iconbitmap(ico_path)
root.after(200, lambda: root.wm_iconbitmap(ico_path))

root.title("BankStatement Pro")
root.state("zoomed")
root.minsize(860, 600)
root.configure(bg=BG)

# ── Outer layout
outer = tk.Frame(root, bg=BG)
outer.pack(expand=True, fill="both", padx=0, pady=0)

# ── Card
card = tk.Frame(outer, bg=CARD_BG, bd=0,
                highlightthickness=1, highlightbackground=BORDER)
card.place(relx=0.5, rely=0.5, anchor="center", width=680, height=620)

# ── Header
header = tk.Frame(card, bg=PRIMARY, height=72)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="DeJay INFOTECH",
         font=("Segoe UI", 9, "bold"),
         fg="#93C5FD", bg=PRIMARY).pack(pady=(14, 0))
tk.Label(header, text="BankStatement Pro",
         font=("Segoe UI", 16, "bold"),
         fg="white", bg=PRIMARY).pack()

# ── Step indicators
step_bar = tk.Frame(card, bg=CARD_BG, pady=16)
step_bar.pack(fill="x", padx=40)

step_circles = []
step_labels  = []
step_names   = ["Select Bank", "Upload PDF", "Process"]

for i, name in enumerate(step_names):
    col = tk.Frame(step_bar, bg=CARD_BG)
    col.pack(side="left", expand=True)

    c = tk.Canvas(col, width=28, height=28, bg=CARD_BG, highlightthickness=0)
    c.pack()
    step_circles.append(c)

    lbl = tk.Label(col, text=name, font=FONT_STEP, bg=CARD_BG, fg=MUTED)
    lbl.pack()
    step_labels.append(lbl)

    if i < 2:
        line_frame = tk.Frame(step_bar, bg=BORDER, height=2, width=60)
        line_frame.pack(side="left", expand=True, pady=10)

update_steps(1)

# Divider
tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=20)

# ── Body
body = tk.Frame(card, bg=CARD_BG, padx=36, pady=10)
body.pack(fill="both", expand=True)

# ── Step 1: Select Bank
tk.Label(body, text="1  SELECT BANK",
         font=FONT_LABEL, fg=MUTED, bg=CARD_BG).pack(anchor="w", pady=(8, 6))

bank_grid = tk.Frame(body, bg=CARD_BG)
bank_grid.pack(fill="x")

for idx, bank in enumerate(BANK_LIST):
    row = idx // 2
    col = idx % 2

    btn_frame = tk.Frame(bank_grid, bg=CARD_BG,
                         highlightthickness=1, highlightbackground=BORDER,
                         cursor="hand2")
    btn_frame.grid(row=row, column=col, padx=4, pady=3, sticky="ew")
    bank_grid.columnconfigure(col, weight=1)

    indicator = tk.Label(btn_frame, text="", width=2,
                         bg=BORDER, font=FONT_SMALL)
    indicator.pack(side="left", fill="y", ipadx=4)

    tk.Label(btn_frame, text=bank,
             font=FONT_BODY, bg=CARD_BG, fg=TEXT_MID,
             padx=10, pady=6, anchor="w").pack(side="left", fill="x", expand=True)

    bank_buttons[bank] = (btn_frame, indicator)

    btn_frame.bind("<Button-1>", lambda e, b=bank: on_bank_select(b))
    for child in btn_frame.winfo_children():
        child.bind("<Button-1>", lambda e, b=bank: on_bank_select(b))

# ── Step 2: Upload PDF
tk.Label(body, text="2  UPLOAD PDF",
         font=FONT_LABEL, fg=MUTED, bg=CARD_BG).pack(anchor="w", pady=(12, 4))

upload_btn_frame = make_button(body, "⬆  Upload PDF", upload_file,
                                bg=ACCENT, width=240, height=36)
upload_btn_frame.pack(anchor="w")
upload_btn_frame.grid_remove = upload_btn_frame.pack_forget
upload_btn_frame.grid        = upload_btn_frame.pack
upload_btn_frame.pack_forget()

# File display
file_display_frame = tk.Frame(body, bg="#F0FDF4",
                               highlightthickness=1, highlightbackground="#86EFAC")
file_display_frame.pack(anchor="w", fill="x", pady=4)
file_display_frame.pack_forget()

tk.Label(file_display_frame, text="📄", font=("Segoe UI", 11),
         bg="#F0FDF4", fg=SUCCESS).pack(side="left", padx=(8, 4), pady=4)

file_name_label = tk.Label(file_display_frame, text="",
                            font=FONT_BODY, bg="#F0FDF4", fg=SUCCESS)
file_name_label.pack(side="left", pady=4)

tk.Button(file_display_frame, text="✖", command=remove_file,
          bg="#F0FDF4", fg=DANGER, bd=0,
          font=("Segoe UI", 9), cursor="hand2").pack(side="right", padx=8)

file_display_frame.grid_remove = file_display_frame.pack_forget
file_display_frame.grid        = lambda: file_display_frame.pack(anchor="w", fill="x", pady=4)

# ── Step 3: Process
tk.Label(body, text="3  PROCESS",
         font=FONT_LABEL, fg=MUTED, bg=CARD_BG).pack(anchor="w", pady=(10, 4))

process_btn_frame = make_button(body, "▶  Process File", process_file,
                                 bg=SUCCESS, width=240, height=36)
process_btn_frame.pack(anchor="w")
process_btn_frame.grid_remove = process_btn_frame.pack_forget
process_btn_frame.grid        = process_btn_frame.pack
process_btn_frame.pack_forget()

# Loading
loading_frame = tk.Frame(body, bg=CARD_BG)
loading_frame.pack(anchor="w")
loading_frame.pack_forget()

tk.Label(loading_frame, text="⏳  Processing, please wait...",
         font=FONT_BODY, fg=ACCENT, bg=CARD_BG).pack(side="left", pady=4)

loading_frame.grid_remove = loading_frame.pack_forget
loading_frame.grid        = loading_frame.pack

# ── Clear button
clear_frame = tk.Frame(body, bg=CARD_BG)
clear_frame.pack(anchor="w", pady=(8, 0))

tk.Button(clear_frame, text="Clear All", command=clear_all,
          font=FONT_SMALL, fg=MUTED, bg=CARD_BG, bd=0,
          cursor="hand2", activeforeground=DANGER,
          activebackground=CARD_BG).pack()

# ── Status bar
status_bar = tk.Frame(card, bg="#F8FAFC",
                       highlightthickness=1, highlightbackground=BORDER,
                       height=30)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

status_var = tk.StringVar(value="Select a bank to get started.")
tk.Label(status_bar, textvariable=status_var,
         font=FONT_STATUS, fg=MUTED, bg="#F8FAFC",
         anchor="w").pack(side="left", padx=12, fill="both")

root.mainloop()