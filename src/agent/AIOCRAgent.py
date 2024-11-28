import os

from fastapi import UploadFile
from src.domain.BO import AIVLBo
from src.venum.DocTypeEnum import DocTypeEnum
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
    if aivlBo.docType == DocTypeEnum.IMG.value:
        img_path = FileUtil.save_file(file)
        print("img_path:", img_path)
        result = QwenVL.vl_ocr(img_path, aivlBo.prompt, aivlBo.returnType)
        result = result[0].replace("```markdown", "").replace("```", "")
        return result
    elif aivlBo.docType == DocTypeEnum.PDF.value:
        img_paths = PDFUtil.pdf_to_images(file)
        results = []
        for img_path in img_paths:
            print("img_path:", img_path)
            result = QwenVL.vl_ocr(img_path, aivlBo.prompt, aivlBo.returnType)
            result = result[0].replace("```markdown", "").replace("```", "")
            results.append(result)
        return ''.join(results)
    else:
        return "Document type not supported."
