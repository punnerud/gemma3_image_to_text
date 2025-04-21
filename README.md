# Gemma 3 Image to Text

A web application that uses Gemma 3 to extract text from images. The application allows you to select a portion of an image and get the text content from that selection.

## Features

- Upload and select portions of images
- Extract text using Gemma 3
- Real-time processing time estimation
- Option to include/exclude context image
- Progress tracking with countdown timer

## Example

![Example of text extraction](https://punnerud.github.io/gemma3_image_to_text/example.png)

1. Upload an image
2. Select the area containing text
3. Choose whether to include context
4. Click "Analyze Selection" to extract text

## Setup

1. Clone the repository
2. Install dependencies
3. Run the Flask application
4. Open in browser at `http://localhost:7000`

## Requirements

- Python 3.x
- Flask
- Ollama with Gemma 3 model

## License

MIT License 