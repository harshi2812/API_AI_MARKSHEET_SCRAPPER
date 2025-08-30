import io
import os
import math
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import cv2
import numpy as np

# Import your other local python files
import schemas
import llm_handler

# --- Configuration Section ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_bin_path = r"C:\poppler-25.07.0\Library\bin"
# -----------------------------

# --- OCR Processing Logic ---
def process_file_and_extract_text(contents: bytes, filename: str) -> str:
    """
    Handles file processing with a single, robust pre-processing pipeline.
    """
    def preprocess_image(image):
        """Applies a robust pre-processing pipeline to the image."""
        np_image = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
        
        # Apply intelligent denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        return Image.fromarray(thresh)

    tesseract_config = '--oem 3 --psm 6'
    extracted_text = ""
    file_lower = filename.lower()

    try:
        if file_lower.endswith(".pdf"):
            images = convert_from_bytes(contents, dpi=300, poppler_path=poppler_bin_path)
            for i, image in enumerate(images):
                processed_image = preprocess_image(image)
                extracted_text += f"--- Page {i+1} ---\n"
                extracted_text += pytesseract.image_to_string(processed_image, lang='eng+hin', config=tesseract_config) + "\n"
        
        elif file_lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image = Image.open(io.BytesIO(contents))
            processed_image = preprocess_image(image)
            extracted_text = pytesseract.image_to_string(processed_image, lang='eng+hin', config=tesseract_config)
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

    except Exception as e:
        # Catch potential errors from processing and raise a clear HTTP exception
        raise HTTPException(status_code=500, detail=f"An error occurred during OCR processing: {e}")

    return extracted_text

# --- FastAPI Application ---
app = FastAPI(title="AI Marksheet Extraction API")

@app.post("/extract/", response_model=schemas.MarksheetData)
async def extract_text_from_file(file: UploadFile = File(...)):
    contents = await file.read()
    raw_text = process_file_and_extract_text(contents, file.filename)
    if not raw_text.strip():
        raise HTTPException(status_code=422, detail="OCR failed to extract any text from the document.")
    structured_data = llm_handler.get_structured_data_from_llm(raw_text)
    if "error" in structured_data:
        raise HTTPException(status_code=500, detail=structured_data["error"])
    return structured_data

