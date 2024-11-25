import fitz
from fastapi import UploadFile
import os

from src.util import FileUtil
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")


def pdf_to_images(file: UploadFile):

    # Save file
    pdf_file_path = FileUtil.save_file(file)
    print("pdf_file_path=", pdf_file_path)

    # Output images path
    pdf_save_dir = os.path.dirname(pdf_file_path)
    print("pdf_save_dir=", pdf_save_dir)

    pdf_images_directory = f"{pdf_save_dir}/imgs"
    os.makedirs(pdf_images_directory, exist_ok=True)

    # Convert
    pdf = fitz.open(pdf_file_path)
    image_paths = []
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        pix = page.get_pixmap()
        image_file_path = f'{pdf_images_directory}/page_{page_number + 1}.jpg'
        image_paths.append(image_file_path)
        pix.save(image_file_path)
    return image_paths
