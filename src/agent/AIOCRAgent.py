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
    rt_result = ""
    if aivlBo.docType == DocTypeEnum.IMG.value:
        img_path = ""
        if aivlBo.fileURL != "":
            img_path = aivlBo.fileURL
        else:
            img_path = FileUtil.save_file(file)
        print("img_path:", img_path)
        result = QwenVL.vl_ocr(img_path, aivlBo.prompt, aivlBo.returnType)
        rt_result = result[0]
    elif aivlBo.docType == DocTypeEnum.PDF.value:

        # File URL
        if aivlBo.fileURL != "":
            status, filepath = FileUtil.download_pdf(aivlBo.fileURL)
            if not status:
                return f"Download PDF Failed,file_url={filepath}"
            else:
                file = FileUtil.file_to_upload_file(filepath)

        img_paths = PDFUtil.pdf_to_images(file)
        results = []
        index = 1
        pdf_length = len(img_paths)
        for img_path in img_paths:
            print(f"{index}/{pdf_length}:", img_path)
            result = QwenVL.vl_ocr(img_path, aivlBo.prompt, aivlBo.returnType)
            result = result[0]
            results.append(result)
            index += 1
        rt_result = ''.join(results)
    else:
        return "Document type not supported."

    return rt_result.replace("```markdown", "").replace("```", "")