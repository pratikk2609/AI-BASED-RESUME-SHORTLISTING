from fastapi import FastAPI, HTTPException, UploadFile, File, Query
import fitz


def extract_pdf_text(pdf_file: UploadFile) -> str:
    try:
        pdf_document = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        one_line_text = " ".join(text.split())
        return one_line_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {e}")