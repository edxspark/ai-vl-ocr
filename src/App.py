#!/usr/bin/venv python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm.PhiVL import PhiVL
from src.agent import AIOCRAgent
from src.domain.BO import AIVLBo
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI-VL-OCR",
    version="1.0",
    description="Open source project for OCR based on AI vision.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Upload file
@app.post("/ai/vl/ocr")
def ai_vl_ocr(docType: str = Form(...),returnType: str = Form(...), prompt: str = Form(...), file: UploadFile = File(...)):
    aivlBo = AIVLBo(docType=docType, returnType=returnType, prompt=prompt, file=file)
    print("#####ai_vl_ocr BEG")
    result = AIOCRAgent.ai_vl_ocr(aivlBo, file)
    print(result[0])
    print("#####ai_vl_ocr END")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)
