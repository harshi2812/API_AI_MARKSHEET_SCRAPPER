AI Marksheet Extraction API
This project is an AI-powered API built with Python and FastAPI that extracts structured data from marksheet images and PDFs. It uses a robust OCR pipeline and the Google Gemini LLM to parse document text into a clean JSON format, including confidence scores for each extracted field.

Features
File Support: Accepts PDF, JPG, PNG, and WEBP files.

Advanced OCR: Utilizes an advanced image pre-processing pipeline (denoising, adaptive thresholding) to handle both clean and difficult-to-read documents.

AI-Powered Extraction: Uses Google's gemini-1.5-flash-latest model to intelligently extract fields and generate confidence scores in a single API call.

Structured JSON Output: Returns a consistent, well-defined JSON structure as defined by Pydantic schemas.

Robust Error Handling: Provides clear error messages for invalid file types, large files, and processing failures.

API Endpoint
POST /extract/
Upload a marksheet file to this endpoint to receive the extracted JSON data.

Example curl Request:

curl -X POST "[http://127.0.0.1:8000/extract/](http://127.0.0.1:8000/extract/)" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@/path/to/your/marksheet.pdf"

Setup and Run Locally
Clone the repository:
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName

Create and activate a virtual environment:
python -m venv venv
.\venv\Scripts\activate (Windows)

Install dependencies:
pip install -r requirements.txt

Set up environment variables:

Create a file named .env.

Add your Google Gemini API key: GOOGLE_API_KEY="your_api_key_here"

Run the application:
uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.