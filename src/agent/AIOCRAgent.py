from src.domain.BO import AIVLBo
from src.enum.DocTypeEnum import DocTypeEnum


# AI VL OCR
# 1. Type switch
# 2. Document to images
# 3. To Call function of AI VL OCR
# 4. Return markdown
def ai_vl_ocr(aivlBo: AIVLBo):
    if aivlBo.docType == DocTypeEnum.IMG.value:
        return "IMG"
    elif aivlBo.docType == DocTypeEnum.PDF.value:
        return "PDF"
    else:
        return "Document type not supported."
