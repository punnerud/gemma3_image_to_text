from flask import Flask, render_template, request, jsonify
import ollama
import os
import base64
from werkzeug.utils import secure_filename
import tempfile
import logging
import re
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_json_and_description(text):
    """Extract JSON content and additional description from the text."""
    try:
        # Try to find JSON pattern first
        json_match = re.search(r'\{[\s\n]*"markedText"[\s\n]*:[\s\n]*"([^"]*)"[\s\n]*\}', text)
        
        if json_match:
            marked_text = json_match.group(1)
            # Get any text before and after the JSON as description
            full_json = json_match.group(0)
            description = text.replace(full_json, '').strip()
            return {
                'markedText': marked_text,
                'description': description if description else None
            }
        else:
            # If no JSON found, treat entire text as description
            return {
                'markedText': None,
                'description': text.strip()
            }
    except Exception as e:
        logger.error("Error parsing response: %s", str(e))
        return {
            'markedText': None,
            'description': text.strip()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        logger.debug("Received request data keys: %s", data.keys() if data else "No data")
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        required_fields = ['markedImage', 'croppedImage', 'selection']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Create temporary files for both images
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as marked_file, \
             tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as cropped_file:
            try:
                # Decode and save marked image
                try:
                    marked_data = data['markedImage'].split(',')[1]
                    marked_file.write(base64.b64decode(marked_data))
                    marked_file.flush()
                    marked_path = marked_file.name

                    # Decode and save cropped image
                    cropped_data = data['croppedImage'].split(',')[1]
                    cropped_file.write(base64.b64decode(cropped_data))
                    cropped_file.flush()
                    cropped_path = cropped_file.name

                    logger.debug("Successfully wrote images to %s and %s", marked_path, cropped_path)
                except Exception as e:
                    logger.error("Error processing images: %s", str(e))
                    return jsonify({'error': f'Error processing images: {str(e)}'}), 500

                # Get image description using Ollama
                try:
                    response = ollama.chat(
                        model='gemma3:27b-it-qat',
                        messages=[
                            {
                                'role': 'user',
                                'content': f'I have two images from a document. The second image is a cropped section containing text that I want you to extract. The first image shows the full document with this section marked in red. Please respond with ONLY the exact text from the cropped section in this JSON format: {{"markedText": "extracted text here"}}. If you notice anything else interesting or relevant about the text or its context, you can add that as plain text after the JSON.',
                                'images': [marked_path, cropped_path]
                            }
                        ]
                    )
                    logger.debug("Successfully got response from Ollama")
                    
                    # Parse the response
                    parsed_response = extract_json_and_description(response['message']['content'])
                    return jsonify(parsed_response)
                    
                except Exception as e:
                    logger.error("Error from Ollama API: %s", str(e))
                    return jsonify({'error': f'Error from Ollama API: {str(e)}'}), 500
                
            finally:
                # Clean up temporary files
                try:
                    os.unlink(marked_path)
                    os.unlink(cropped_path)
                    logger.debug("Successfully cleaned up temporary files")
                except Exception as e:
                    logger.warning("Error cleaning up temporary files: %s", str(e))
            
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7000) 