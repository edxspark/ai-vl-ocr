import os

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

# These values will be rounded to the nearest multiple of 28.
min_pixels = 256 * 28 * 28
max_pixels = 1280 * 28 * 28
processor = AutoProcessor.from_pretrained(model_dir, min_pixels=min_pixels, max_pixels=max_pixels)

# No GPU
# model = None
# processor = None


class QwenVL:

    @staticmethod
    def vl_ocr(img_paths: [], prompt: str, returnType: str):

        # Prompt
        vl_prompt = f"""
        ```{prompt}```
        
        # RESPONSE #
        Output format: ```{returnType}```
        """

        print("#####prompt:", vl_prompt)

        # Content
        content = []
        for img_path in img_paths:

            img = {
                "type": "image",
                "image": img_path,
            }
            content.append(img)
        content.append({"type": "text", "text": vl_prompt})
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
        generated_ids = model.generate(**inputs, max_new_tokens=10240)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        return output_text



