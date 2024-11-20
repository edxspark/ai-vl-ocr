from fastapi import UploadFile
from pydantic import BaseModel


class AIVLBo(BaseModel):
    docType: str
    returnType: str
    prompt: str
    file: UploadFile