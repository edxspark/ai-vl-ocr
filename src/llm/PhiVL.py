import os
from PIL import Image
import requests
from transformers import AutoModelForCausalLM, AutoProcessor
from dotenv import load_dotenv
from modelscope import snapshot_download
load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")

model_root = f"{STORAGE_PATH}/models"
model_name = 'AI-ModelScope/Phi-3.5-vision-instruct'
os.environ['MODELSCOPE_CACHE'] = model_root
model_dir = snapshot_download(model_name, revision='master')


class PhiVL:
    def __init__(self, model_id=f"{model_root}/hub/Phi-3___5-vision-instruct", device="cuda"):
        """
        使用指定的模型 ID 和设备初始化 Phi3VisionModel。

        参数：
            model_id (str): 来自 Hugging Face 模型库的预训练模型标识符。
            device (str): 加载模型的设备（"cuda" 表示 GPU，或 "cpu"）。
        """
        self.model_id = model_id
        self.device = device
        self.model = self.load_model()  # 在初始化时加载模型
        self.processor = self.load_processor()  # 在初始化时加载处理器

    def load_model(self):
        """
        加载具有因果语言建模能力的预训练语言模型。

        返回：
            model (AutoModelForCausalLM): 加载的模型。
        """
        print("加载模型中...")
        # 使用自动设备映射和数据类型调整加载模型
        return AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",  # 自动将模型映射到适当的设备
            torch_dtype="auto",  # 根据设备使用合适的 torch 数据类型
            trust_remote_code=True,  # 允许执行自定义代码以加载模型
            _attn_implementation='flash_attention_2'  # 使用优化的注意力实现
        ).to(self.device)  # 将模型移动到指定设备

    def load_processor(self):
        """
        加载与模型关联的处理器，以处理输入和输出。

        返回：
            processor (AutoProcessor): 用于处理文本和图像的加载处理器。
        """
        print("加载处理器中...")
        # 使用 trust_remote_code=True 加载处理器，以处理任何自定义处理逻辑
        return AutoProcessor.from_pretrained(self.model_id, trust_remote_code=True)

    def predict(self, image_url, prompt):
        """
        使用模型根据给定的图像和提示进行预测。

        参数：
            image_url (str): 要处理的图像的 URL。
            prompt (str): 指导模型生成的文本提示。

        返回：
            response (str): 模型生成的响应。
        """
        # 从提供的 URL 加载图像
        image = Image.open(requests.get(image_url, stream=True).raw)

        # 为模型格式化输入提示模板
        prompt_template = f"<|user|>\n<|image_1|>\n{prompt}<|end|>\n<|assistant|>\n"

        # 处理输入，将提示和图像转换为张量格式
        inputs = self.processor(prompt_template, [image], return_tensors="pt").to(self.device)

        # 设置模型响应生成的参数
        generation_args = {
            "max_new_tokens": 500,  # 最大生成的令牌数
            "temperature": 0.7,     # 生成中的采样温度以增加多样性
            "do_sample": False      # 禁用采样以获得确定性输出
        }
        print("生成响应中...")
        # 使用模型生成输出 ID，跳过输入令牌
        output_ids = self.model.generate(**inputs, **generation_args)
        output_ids = output_ids[:, inputs['input_ids'].shape[1]:]  # 忽略输出中的输入提示

        # 解码生成的输出令牌以获取响应文本
        response = self.processor.batch_decode(output_ids, skip_special_tokens=True)[0]
        return response

    def vl_ocr(self, image_url):
        image_url = image_url  # 示例图像的 URL
        prompt = "以 json 格式提取数据。"  # 模型指导的提示
        response = self.predict(image_url, prompt)  # 从模型获取响应
        print("响应:", response)  # 打印生成的响应
        return response
