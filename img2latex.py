import openai
from qwen_api import LlmApi
from typing import List


def img2latex(model: str, api_key: str, base_url: str, prompt_list: List[dict], proxy: str = None) -> str:
    """主函数：调用 LLM API 进行图片到 LaTeX 的转换"""
    openai.proxy = proxy  # 可选的代理设置
    openai.api_key = api_key
    openai.api_base = base_url

    qwen_vl_ocr_latest = LlmApi(
        api_key=openai.api_key,
        base_url=openai.api_base,
        model=model,
        proxy=openai.proxy  # 使用代理
    )

    prompt_list = prompt_list

    answer = qwen_vl_ocr_latest.get_response(prompt_list)

    return answer


if __name__ == "__main__":
    latex = img2latex(
        api_key="sk-fdcf1779455c4453af36562cf4678690",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen2.5-vl-72b-instruct",
        proxy="http://127.0.0.1:26561",  # 使用代理
        prompt_list=[
            {
                "type": "text",
                "text": """
                你是一个专业的LaTeX公式识别专家。
                请将图片中的数学公式准确转换为LaTeX代码。
                要求：
                1. 只返回标准LaTeX代码，不包含任何解释或说明，可以直接嵌入到HTML文档中
                2. 公式两边不需要加入任何额外的数学环境标记(如 \\[ \\] 或 \\( \\) 等)
                3. 如果公式末尾包含类似 ( 2 - 1 ) 这样的公式编号，请将这部分去掉
                """
            },
            {
                "type": "image_url",
                "image_url": "./formula.png"
            }
        ]
    )

    print(latex)
