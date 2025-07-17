# 🧾 Smart Document OCR API

A FastAPI-based backend that extracts structured fields (e.g., receipt ID, date, total, and change) from uploaded images or PDFs using OCR and regex-based layout parsing.

---

## 🚀 Features

- 📤 Upload image or PDF receipt/invoice
- 🧹 Preprocess for optimal OCR accuracy
- 🔍 OCR with Tesseract
- 📄 Field extraction using customizable regex rules
- ⚡ FastAPI backend with `/extract` endpoint
- 🧪 Unit-tested components

---

## 🧠 Technologies

- Python 3.10+
- FastAPI
- Tesseract OCR (via pytesseract)
- OpenCV (image processing)
- PDF2Image (PDF to image conversion)
- Regex-based field parsing

---

## 📂 Project Structure

``` bash
app/
├── main.py → FastAPI app
├── ocr_engine/ → OCR Module
    ├── ocr_engine.py → Text extraction using Tesseract
├── preprocess/ → Image Preprocessing Module
    ├── image_preprocessor.py → Image cleaning pipeline
├── layout_parser/ → Layout Parser Module
    ├── layout_parser.py →  Regex-based field extractor

data/ → Sample images

```

## 🔧 Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/smart-doc-ocr.git
cd smart-doc-ocr
```

### 2. Install dependencies

Use a virtual environment if needed.

``` bash
pip install -r requirements.tx
```

### 3. Install Systme dependencies

Follow below link to install `Pytesseract` across different platforms

[Introduction to Python Pytesseract Package](https://www.geeksforgeeks.org/python/introduction-to-python-pytesseract-package/)

## 🔄 To Do (Next Steps)

- Dockerize the app
- Add frontend interface (e.g., Streamlit or React)
- Export results as JSON/CSV
