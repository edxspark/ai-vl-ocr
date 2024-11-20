#!/usr/bin/venv python
import os
import sys

from pydantic import BaseModel

from src.agent import AIOCRAgent
from src.domain.BO import AIVLBo

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
def ai_vl_ocr(aivlBo:AIVLBo):
    return AIOCRAgent.ai_vl_ocr(aivlBo)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)
