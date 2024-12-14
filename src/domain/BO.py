
from pydantic import BaseModel


class AIVLBo(BaseModel):
    docType: str
    returnType: str
    prompt: str
    fileURL: str

class AIVLPdfBo(BaseModel):
    prompt: str
    fileURL: str