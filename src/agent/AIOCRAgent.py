import os

from fastapi import UploadFile
from src.domain.BO import AIVLBo
from src.enum.DocTypeEnum import DocTypeEnum
from src.llm.QwenVL import QwenVL
from src.util import FileUtil, PDFUtil
from dotenv import load_dotenv
load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")


# AI VL OCR
# 1. Type switch
# 2. Document to images
# 3. To Call function of AI VL OCR
# 4. Return markdown
def ai_vl_ocr(aivlBo: AIVLBo, file: UploadFile):
    img_paths = []
    if aivlBo.docType == DocTypeEnum.IMG.value:
        img_path = FileUtil.save_file(file)
        img_paths.append(img_path)
        return QwenVL.vl_ocr(img_paths, aivlBo.prompt, aivlBo.returnType)
    elif aivlBo.docType == DocTypeEnum.PDF.value:
        img_paths = PDFUtil.pdf_to_images(file)
        return QwenVL.vl_ocr(img_paths, aivlBo.prompt, aivlBo.returnType)
    else:
        return "Document type not supported."
