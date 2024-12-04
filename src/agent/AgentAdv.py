import os
import uuid

from PIL import Image
from fastapi import UploadFile

from dotenv import load_dotenv

from src.llm.QwenVL import QwenVL
from src.util import ImageUtil

load_dotenv()

STORAGE_PATH = os.getenv("STORAGE_PATH")
adv_dir_path = f"{STORAGE_PATH}/adv"


def adv_upload(file: UploadFile):
    file_name, file_extension = os.path.splitext(file.filename)

    # 1. 接收压缩包文件
    os.makedirs(adv_dir_path, exist_ok=True)
    file_name_uuid = str(uuid.uuid4())
    file_name_new = f"{file_name_uuid}{file_extension}"
    file_path = f"{adv_dir_path}/{file_name_new}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    image = Image.open(file_path)
    width, height = image.size
    if width > 800 or height > 800:
        print(f"#####:{file_path}")
        print(f"#####图片过大，等比缩放[width={width},height={height}]")
        image_no_alpha = image.convert('RGB')
        image_no_alpha.save(file_path,'JPEG')
        ImageUtil.resize_image(file_path,file_path,800)
    return {"file_id": file_name_new}


def adv_compare(img_file_name1, img_file_name2):
    img_path1 = f"{adv_dir_path}/{img_file_name1}"
    img_path2 = f"{adv_dir_path}/{img_file_name2}"
    return QwenVL.vl_compare(img_path1, img_path2)
