# BankStatement Pro

![Tests](https://github.com/devayani24/PDF-to-Excel-Pipeline/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/devayani24/PDF-to-Excel-Pipeline/actions/workflows/release.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)

A production desktop tool built for an accounting firm to automate bank statement processing — reducing manual data entry from hours to seconds.

---

## 🎯 Business Problem Solved

Accounting firms process hundreds of bank statements monthly. Each statement requires manually copying transaction data into spreadsheets — a slow, error-prone process.

**BankStatement Pro** extracts transaction data from bank PDFs automatically, cutting processing time by **~95%** and eliminating manual entry errors.

---

## 📈 Impact

- **7 banks supported** — Indian Bank, SBI, Kotak, Canara, HDFC, KVB, City Union Bank
- **Deployed to a live client** — actively used in production
- **Handles 800+ transactions** per statement reliably
- **Reconciliation validation** — verifies extracted data mathematically before export

---

## 🛠️ Tech Stack

```
Python 3.11 · pdfplumber · pandas · tkinter
pytest · GitHub Actions · PyInstaller · Inno Setup
```

---

## ✅ Engineering Highlights

- **Two parser architectures** — text extraction and coordinate-based, chosen per bank's PDF structure
- **Config-driven design** — adding a new bank requires 15 lines of config, no logic changes
- **78% test coverage** with unit, integration and real data validation tests
- **CI/CD pipeline** — automated testing on every push, automated .exe build and GitHub Release on every tag
- **Professional installer** built with Inno Setup — ships like real software

---

## 📸 Screenshots

> *(Add screenshot here)*

---

## 🔗 Links

- [Latest Release](https://github.com/devayani24/PDF-to-Excel-Pipeline/releases/latest)
