import os

from PIL import Image
from qwen_vl_utils import process_vision_info
from modelscope import snapshot_download
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")
AI_VL_MODEL = os.getenv("AI_VL_MODEL")


# GPU
os.environ['MODELSCOPE_CACHE'] = f"{STORAGE_PATH}/models"
model_dir = snapshot_download(AI_VL_MODEL)
model = Qwen2VLForConditionalGeneration.from_pretrained(model_dir, torch_dtype="auto", device_map="auto")
processor = AutoProcessor.from_pretrained(model_dir)

# No GPU
# model = None
# processor = None


class QwenVL:

    @staticmethod
    def vl_ocr(img_paths: [], prompt: str, returnType: str):

        # Prompt
        prompt = f"""
        ```{prompt}```
        
        # RESPONSE #
        Output format: ```{returnType}```
        """

        # Content
        content = []
        for img_path in img_paths:
            max_width = 1000
            max_height = 1000
            image = Image.open(img_path)
            width, height = image.size
            if width > max_width:
                width = max_width
            if height > max_height:
                height = max_height
            img = {
                "type": "image",
                "resized_height": height,
                "resized_width": width,
                "image": img_path,
            }
            content.append(img)
        content.append({"type": "text", "text": prompt})
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]

        # Preparation for inference
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Inference: Generation of the output
        generated_ids = model.generate(**inputs, max_new_tokens=384)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        return output_text



