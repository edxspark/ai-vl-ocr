import os
import uuid

from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")


def save_file(file: UploadFile):
    file_name_uuid = str(uuid.uuid4())
    file_dir = f"{STORAGE_PATH}/{file_name_uuid}/imgs"
    os.makedirs(file_dir, exist_ok=True)
    file_name, file_extension = os.path.splitext(file.filename)
    file_name_new = f"{file_name_uuid}{file_extension}"
    file_save_path = f"{file_dir}/{file_name_new}"
    with open(file_save_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_save_path


if __name__ == '__main__':
    markdown = "```markdown\n# Frank Benade (54)\n\n## Counselor / Psychologist and TEFL Teacher (Face to face and online)\n\n### Profile\nAt Lylac, I serve as a counselor driven by an unwavering commitment to fostering understanding and connection. My journey, rooted in a personal quest to overcome feelings of being misunderstood, has led me to the field of counseling. I firmly believe in the transformative power of effective communication. With TEFL and CPA certifications, I am equipped to empower individuals of all ages through both counseling and teaching. My expertise extends to online English teaching, where I strive to create engaging and effective learning experiences for students around the world. I am eager to bring my skills and passion to your vibrant learning community, where I hope to ignite positive change and facilitate growth for all.\n\n### Work Experience\n\n| Year | Company | Position |\n|------|---------|----------|\n| 2016 - 2024 | Lylac.org | Counselor / Psychologist / Teacher |\n| 2014 - 2016 | Lylac.org | Mentor and Counselor for Adults |\n\n#### Lylac.org\n- **Counselor / Psychologist / Teacher**: Passionate counselor and psychologist dedicated to fostering healing and personal growth through online one-to-one teaching and support, including online English teaching.\n- **Specialized expertise in trauma, marriage, and relationship counseling, delivering sessions with deep empathy and keen insight.**\n- **Proven track record as a transformative agent, guiding clients from despair to resilience with a compassionate approach.**\n- **Skilled life coach, inspiring individuals to unlock their potential and overcome life's challenges with determination and clear vision.**\n- **Recognized as a steadfast source of hope, assisting clients through emotional turmoil towards tranquility and self-empowerment.**\n- **Expertise in trauma and relationship counseling, offering tailored strategies for healing and development.**\n- **Experienced in online English teaching, providing personalized instruction that enhances language skills and fosters effective communication.**\n\n#### Lylac.org\n- **Mentor and Counselor for Adults**: Expertly mentored and counseled adults, driving their personal and professional growth.\n- **Proficiently managed business operations, ensuring seamless organizational efficiency.**\n- **Successfully orchestrated company operations, creating exceptional and memorable experiences.**\n- **Passionate about guiding adults in their career paths, helping them achieve their professional goals.**\n- **Oversaw company operations with a focus on continuous improvement and strategic success.**\n\n### Education\n- **TEFL Certificate / CPA Mathematics**\n- **Ph.D. in Psychology** - University of Pretoria - 1994\n\n### Expertise\n- Psychology\n- Life coaching\n- Business owner\n- SEO\n- TEFL Online Teaching\n\n### Language\n- English\n- Afrikaans\n```"
    print(markdown)