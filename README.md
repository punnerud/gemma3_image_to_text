# Image Description with Gemma 3

This is a simple web application that allows you to upload images and get detailed descriptions using the Gemma 3 27B model.

## Prerequisites

1. Make sure you have Ollama installed and running locally
2. Pull the Gemma 3 model:
   ```bash
   ollama pull gemma3:27b-it-qat
   ```

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:7000
   ```

## Usage

1. Click on the upload area or drag and drop an image file
2. The image will be uploaded and processed by the Gemma 3 model
3. A detailed description of the image will be displayed below

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF

## Notes

- Maximum file size is 16MB
- Images are temporarily stored in the `uploads` directory and automatically deleted after processing
- The application uses the local Ollama instance running on your machine 