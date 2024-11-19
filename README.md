# AI-VL-OCR
A very simple way of OCR-ing a document of AI vision.  
Documents are meant to be a visual representation after all.  
With weird layouts, tables, charts, etc.   
The vision models just make sense!   

The general logic:
- Pass in a file (pdf, docx, image, etc.) 
- Convert that file into a series of images 
- Pass each image to AI vision LLM and ask nicely for Markdown 
- Aggregate the responses and return Markdown

# Getting Started
```
conda create --name ai-vl-ocr python=3.11
conda activate ai-vl-ocr
pip install -r requirements.txt
python src/App.py
```

# Usage
```
http://127.0.0.1:19527
```

# Example Output
