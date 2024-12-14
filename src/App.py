#!/usr/bin/venv python
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.llm.QwenVL import QwenVL
from src.agent import AIOCRAgent, AgentAdv
from src.domain.BO import AIVLBo, AIVLPdfBo
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
    aivlBo = AIVLBo(docType=docType, returnType=returnType, prompt=prompt, fileURL="")
    print("#####ai_vl_ocr BEG")
    result = AIOCRAgent.ai_vl_ocr(aivlBo, file)
    print("result=", result)
    if returnType == "JSON":
        result = result.replace("json", "").replace("```", "")
        result = json.loads(result)

    print("#####ai_vl_ocr END")
    return result

@app.post("/ai/vl/ocr/pdf_url")
def ai_vl_ocr_pdf_url(prompt: str = Form(...), file_url: str = Form(...)):
    aivlPdfBo = AIVLPdfBo(prompt=prompt, fileURL=file_url)
    print("#####ai_vl_ocr_url BEG")
    result = AIOCRAgent.ai_vl_ocr_pdf_url(aivlPdfBo)
    print("result=", result)
    result = result.replace("json", "").replace("```", "")
    result = json.loads(result)
    print("#####ai_vl_ocr_url END")
    return result


@app.post("/ai/adv/agent/upload")
def adv_upload(file: UploadFile = File(...)):
    return AgentAdv.adv_upload(file)


@app.post("/ai/vl/compare")
def adv_compare(img_url_1: str, img_url_2: str):
    if "http" in img_url_1 or "http" in img_url_2:
        return QwenVL.vl_compare(img_url_1, img_url_2)
    else:
        return AgentAdv.adv_compare(img_url_1, img_url_2)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)
