import json
import os

from qwen_vl_utils import process_vision_info
from modelscope import snapshot_download
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from dotenv import load_dotenv
import torch


load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")
AI_VL_MODEL = os.getenv("AI_VL_MODEL")


# GPU
# os.environ['MODELSCOPE_CACHE'] = f"{STORAGE_PATH}/models/hub"
# model_dir = snapshot_download(AI_VL_MODEL)

model_path = f"{STORAGE_PATH}/models/hub/Qwen/Qwen2-VL-7B-Instruct"
model = Qwen2VLForConditionalGeneration.from_pretrained(model_path,
                                                        torch_dtype=torch.bfloat16,
                                                        attn_implementation="flash_attention_2",
                                                        device_map="auto")

# These values will be rounded to the nearest multiple of 28.
min_pixels = 256 * 28 * 28
max_pixels = 1080 * 28 * 28
processor = AutoProcessor.from_pretrained(model_path,
                                          min_pixels=min_pixels,
                                          max_pixels=max_pixels)

# No GPU
# model = None
# processor = None


class QwenVL:

    @staticmethod
    def vl_ocr(img_path, prompt: str, returnType: str):

        # Prompt
        vl_prompt = f"""
        {prompt}
        
        # RESPONSE #
        Output format: {returnType}
        """

        #print("prompt:", vl_prompt)

        # Content
        content = []
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
        generated_ids = model.generate(**inputs, max_new_tokens=128000)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        return output_text

    @staticmethod
    def vl_compare(img_path1, img_path2):

        print("###img_path1=", img_path1)
        print("###img_path2=", img_path2)

        prompt = """
           你作为AI视觉助手，帮我判断两张图片的相似度。
           两张图片为广告牌设计稿和实际广告牌，请帮我从内容、文字、布局三个纬度进行分析。

           分别描述两张图片上的信息
           使用json格式输出，格式如下：
           {
              "相似度":"50",
              "第一张分析详情":"",
              "第二张分析详情":""
           }
           """

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": img_path1,
                    },
                    {
                        "type": "image",
                        "image": img_path2,
                    },
                    {"type": "text",
                     "text": prompt
                     },
                ],
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

        result = output_text[0].replace("```json", "").replace("```", "")
        result_json = json.loads(result)
        compare_val = result_json["相似度"].replace("%", "")
        compare_percent = int(compare_val)
        print(f"#####compare_percent={compare_percent}")
        result_json_new = {}
        if compare_percent < 90:
            result_json_new["对比结果"] = "不通过"
        else:
            result_json_new["对比结果"] = "通过"

        for key, value in result_json.items():
            result_json_new[key] = value

        return result_json_new


