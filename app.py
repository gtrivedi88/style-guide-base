import os
import pdfplumber
import docx
import markdown
import re
import gradio as gr
import xml.etree.ElementTree as ET
from transformers import pipeline

# Load the Hugging Face model (trained on passive voice correction)
pipe = pipeline(
    "text2text-generation",
    model="gtrivedi/style-guide-base",
    tokenizer="gtrivedi/style-guide-base"
)

# Safe read function to handle both file-like and text-based uploads (like .md or .adoc)
def safe_read(file):
    # If file is a NamedString-like object (from Gradio), it has a .value attribute
    if hasattr(file, "value"):
        return file.value
    data = file.read()
    return data.decode() if isinstance(data, bytes) else data

# Extract text from supported formats
def extract_text(file):
    ext = os.path.splitext(file.name)[-1].lower()

    if ext == '.txt':
        return safe_read(file)

    elif ext == '.docx':
        doc = docx.Document(file)
        return '\n'.join(p.text for p in doc.paragraphs)

    elif ext == '.pdf':
        with pdfplumber.open(file) as pdf:
            return '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())

    elif ext == '.md':
        text = safe_read(file)
        return re.sub('<[^<]+?>', '', markdown.markdown(text))

    elif ext == '.adoc':
        return safe_read(file)

    elif ext == '.dita':
        content = safe_read(file)
        try:
            root = ET.fromstring(content)
            paragraphs = [elem.text.strip() for elem in root.iter() if elem.tag.endswith('p') and elem.text]
            return '\n'.join(paragraphs)
        except ET.ParseError:
            return "❌ Invalid DITA/XML file."

    else:
        return "❌ Unsupported file format."

# Analyze sentence-by-sentence for passive voice
def analyze_text(input_text):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', input_text) if s.strip()]
    results = []

    for sentence in sentences:
        prompt = f"Rewrite to active voice: {sentence}"
        output = pipe(prompt, max_length=50)[0]["generated_text"]
        if sentence != output:
            results.append(f"❌ {sentence}\n✅ {output}\n")

    if not results:
        return "✅ No passive voice issues found."
    return "\n\n".join(results)

# Main Gradio processing function
def process_file(file):
    text = extract_text(file)
    if "❌" in text:
        return text
    return analyze_text(text)

# Gradio UI
ui = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload .md or .adoc file", file_types=[".md", ".adoc"]),
    outputs="text",
    title="AI model to enforce IBM Style Guide",
    description="Detects and rewrites passive voice in uploaded .md or .adoc files using a custom-trained AI model."
)

ui.launch()
