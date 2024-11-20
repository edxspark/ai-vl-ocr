from fastapi import UploadFile
from pdf2image import convert_from_path
import os

from src.util import FileUtil
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")


def pdf_to_images(file: UploadFile):

    # Save file
    pdf_file_path = FileUtil.save_file(file)

    # Output images path
    file_name, file_extension = os.path.splitext(pdf_file_path)
    pdf_images_directory = f"{STORAGE_PATH}/{file_name}"
    os.makedirs(pdf_images_directory, exist_ok=True)

    # Convert
    image_paths = []
    images = convert_from_path(pdf_file_path)
    for i, page in enumerate(images):
        image_file_path = f'{pdf_images_directory}/page_{i + 1}.jpg'
        image_paths.append(image_file_path)
    return image_paths
