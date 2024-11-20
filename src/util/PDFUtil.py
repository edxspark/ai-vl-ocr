from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_file):
    # PDF文件路径
    pdf_path = 'your_pdf_file.pdf'
    # 输出图片的保存路径
    output_folder = 'output_images'

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 将PDF转换为图片
    images = convert_from_path(pdf_path)

    # 遍历每一页，保存为图片
    for i, page in enumerate(images):
        # 构建图片文件名
        image_filename = f'{output_folder}/page_{i + 1}.jpg'
        # 保存图片
        page.save(image_filename, 'JPEG')

    print(f'PDF转换完成，图片已保存到{output_folder}文件夹。')