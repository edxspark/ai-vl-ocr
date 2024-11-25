
from pydantic import BaseModel


class AIVLBo(BaseModel):
    docType: str
    returnType: str
    prompt: str
