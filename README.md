# IBM Style Guide Correction App

A Gradio-based web application that detects and rewrites sentences according to the IBM Style Guide using a custom-trained Hugging Face model.

## Features

- Supports multiple file formats: `.txt`, `.docx`, `.pdf`, `.md`, `.adoc`, `.dita`
- Detects issues sentence-by-sentence and provides rewrites
- Simple Gradio UI for easy file uploads and results viewing

## Prerequisites

- Python 3.7 or higher
- Git
- (Optional) Hugging Face CLI for model access

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**

   ```bash
   python app.py
   ```

2. **Open the Gradio interface**
   
   After running, the terminal will display a local URL (e.g., http://127.0.0.1:7860). Open it in your browser.

3. **Upload a file**
   
   Use the file upload widget to select a supported file. The app will extract text, detect issues, and display corrections.

## Supported File Formats

- `.txt`: Plain text files
- `.docx`: Microsoft Word documents
- `.pdf`: PDF files
- `.md`: Markdown files (HTML tags are stripped)
- `.adoc`: AsciiDoc files
- `.dita`: DITA XML files (extracts `<p>` paragraph text)

## Model Details

This app uses the Hugging Face model `gtrivedi/style-guide-base` (with its corresponding tokenizer) for correction:

```python
from transformers import pipeline

pipe = pipeline(
    "text2text-generation",
    model="gtrivedi/style-guide-base",
    tokenizer="gtrivedi/style-guide-base"
)
```

## Project Structure

```
├── app.py             # Main application file
├── requirements.txt   # Python dependencies
├── .gradio/           # Gradio-specific configurations (do not modify)
├── venv/              # Virtual environment (ignored by Git)
└── README.md          # This file
```

## .gitignore

Include the following in your `.gitignore` to avoid committing environment and config folders:

```
venv/
.gradio/
```

## Google colab .ipnyb book
Review resources directory

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements.

---

*This project is maintained by Gaurav. Feel free to reach out for any questions or feedback.*