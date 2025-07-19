import os
from typing import List
import base64
import json
from dashscope import MultiModalConversation  # 导入DashScope多模态对话接口

import ssl
import urllib3

# 禁用SSL证书验证（全局生效）
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 网络代理
os.environ["HTTP_PROXY"] = "http://127.0.0.1:26561"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:26561"


class LlmApi:
    def __init__(self, api_key: str, model: str):
        # 初始化DashScope（通过环境变量或直接传入API密钥）
        self.api_key = api_key
        self.model = model  # DashScope多模态模型（如qwen-vl-max-latest、qwen2.5-vl-72b-instruct等）

    def get_response(self, prompt_list: List[dict]) -> str:
        """获取LLM响应（适配DashScope MultiModalConversation）"""
        # 构建对话历史（初始仅包含用户的多模态请求）
        messages = [
            {
                "role": "user",
                "content": self.build_content(prompt_list)  # 构建用户内容（文本+图片）
            }
        ]

        # 调用DashScope多模态对话接口
        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages
        )

        # 解析响应结果
        if response.status_code == 200 and response.output.get("choices"):
            print("响应结果:", json.dumps(
                response.output, ensure_ascii=False, indent=2))
            # 提取文本内容（多模态响应的content是列表，取第一个文本元素）
            return response.output["choices"][0]["message"]["content"][0]["text"].strip()
        else:
            raise ValueError(f"请求失败: {response.message}")

    def encode_image(self, image_path: str) -> str:
        """将图片转换为Base64编码（本地图片）"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def build_content(self, prompt_list: List[dict]) -> List[dict]:
        """构建DashScope要求的content格式（文本和图片的组合列表）"""
        content = []
        for item in prompt_list:
            if not isinstance(item, dict):
                raise ValueError("Prompt列表元素必须是字典")

            item_type = item.get("type")
            if item_type == "text":
                # 文本类型：直接添加text字段
                content.append({"text": item["text"]})
            elif item_type == "image_url":
                # 图片类型：支持本地路径（Base64）或网络URL
                image_source = item["image_url"]
                if os.path.exists(image_source):
                    # 本地图片：转换为Base64编码
                    base64_image = self.encode_image(image_source)
                    content.append({
                        # 本地图片Base64格式
                        "image": f"data:image/jpeg;base64,{base64_image}"
                    })
                else:
                    # 网络图片：直接使用URL（需确保模型可访问）
                    content.append({"image": image_source})
            else:
                raise ValueError(f"不支持的类型: {item_type}，仅支持'text'或'image_url'")
        return content


if __name__ == "__main__":
    # 初始化API（替换为你的DashScope API密钥）
    api = LlmApi(
        api_key="sk-fdcf1779455c4453af36562cf4678690",  # 你的DASHSCOPE_API_KEY
        model="qwen-vl-max-latest"  # 推荐使用的多模态模型
    )

    # 构建多模态prompt（文本指令 + 本地图片）
    prompt_list = [
        {
            "type": "text",
            "text": "请将图片中的公式转换为LaTeX代码，仅返回代码，不要其他内容。"
        },
        {
            "type": "image_url",
            "image_url": "./formula.png"  # 本地图片路径（替换为你的图片路径）
            # 若使用网络图片，可改为："image_url": "https://example.com/formula.png"
        }
    ]

    try:
        answer = api.get_response(prompt_list)
        print("LaTeX结果:", answer)
    except Exception as e:
        print("错误:", str(e))
