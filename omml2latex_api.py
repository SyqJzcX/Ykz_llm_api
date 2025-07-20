import openai
from qwen_api import LlmApi
from typing import List


def omml2latex(model: str, api_key: str, base_url: str, omml: str, proxy: str = None) -> str:
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

    prompt_list = [
        {
            "type": "text",
            "text": f"""
                你是一个专业的LaTeX公式识别专家。
                我给出 docx 文档中的公式，格式为 omml，请将其转换为 LaTeX 代码。
                要求：
                1. 只返回标准LaTeX代码，不包含任何解释或说明，可以直接嵌入到HTML文档中
                2. 公式两边不需要加入任何额外的数学环境标记(如 \\[ \\] 或 \\( \\) 等)
                3. 如果公式末尾包含类似 ( 2 - 1 ) 这样的公式编号，请将这部分去掉
                其中 omml 中的 xml 内容为：
                {omml}
                """
        }
    ]

    answer = qwen_vl_ocr_latest.get_response(prompt_list)

    return answer


if __name__ == "__main__":
    omml = """
    <ns0:oMath xmlns:ns0="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:ns1="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <ns0:eqArr>
        <ns0:eqArrPr>
            <ns0:maxDist ns0:val="1" />
            <ns0:ctrlPr>
                <ns1:rPr>
                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                    <ns1:i />
                </ns1:rPr>
            </ns0:ctrlPr>
        </ns0:eqArrPr>
        <ns0:e>
            <ns0:sSub>
                <ns0:sSubPr>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:sSubPr>
                <ns0:e>
                    <ns0:r>
                        <ns0:rPr>
                            <ns0:scr ns0:val="script" />
                        </ns0:rPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>ℒ</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:e>
                <ns0:sub>
                    <ns0:r>
                        <ns0:rPr />
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>CE</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:sub>
            </ns0:sSub>
            <ns0:r>
                <ns0:rPr />
                <ns1:rPr>
                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                </ns1:rPr>
                <ns0:t>∝</ns0:t>
            </ns0:r>
            <ns0:sSup>
                <ns0:sSupPr>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:sSupPr>
                <ns0:e>
                    <ns0:r>
                        <ns0:rPr />
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>N</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:e>
                <ns0:sup>
                    <ns0:r>
                        <ns0:rPr />
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>−α</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                            <ns1:iCs />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:sup>
            </ns0:sSup>
            <ns0:r>
                <ns0:rPr />
                <ns1:rPr>
                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                </ns1:rPr>
                <ns0:t>, N=</ns0:t>
            </ns0:r>
            <ns0:func>
                <ns0:funcPr>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:funcPr>
                <ns0:fName>
                    <ns0:r>
                        <ns0:rPr>
                            <ns0:sty ns0:val="p" />
                        </ns0:rPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>min</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:fName>
                <ns0:e>
                    <ns0:d>
                        <ns0:dPr>
                            <ns0:ctrlPr>
                                <ns1:rPr>
                                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                                    <ns1:i />
                                </ns1:rPr>
                            </ns0:ctrlPr>
                        </ns0:dPr>
                        <ns0:e>
                            <ns0:r>
                                <ns0:rPr />
                                <ns1:rPr>
                                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                                </ns1:rPr>
                                <ns0:t>P,D,C</ns0:t>
                            </ns0:r>
                            <ns0:ctrlPr>
                                <ns1:rPr>
                                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                                    <ns1:i />
                                </ns1:rPr>
                            </ns0:ctrlPr>
                        </ns0:e>
                    </ns0:d>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:e>
            </ns0:func>
            <ns0:r>
                <ns0:rPr />
                <ns1:rPr>
                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                </ns1:rPr>
                <ns0:t>#</ns0:t>
            </ns0:r>
            <ns0:d>
                <ns0:dPr>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:dPr>
                <ns0:e>
                    <ns0:r>
                        <ns0:rPr />
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                        </ns1:rPr>
                        <ns0:t>2−2</ns0:t>
                    </ns0:r>
                    <ns0:ctrlPr>
                        <ns1:rPr>
                            <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                            <ns1:i />
                        </ns1:rPr>
                    </ns0:ctrlPr>
                </ns0:e>
            </ns0:d>
            <ns0:ctrlPr>
                <ns1:rPr>
                    <ns1:rFonts ns1:ascii="Cambria Math" ns1:hAnsi="Cambria Math" />
                    <ns1:i />
                    <ns1:iCs />
                </ns1:rPr>
            </ns0:ctrlPr>
        </ns0:e>
    </ns0:eqArr>
</ns0:oMath>
    """

    latex = omml2latex(
        api_key="sk-fdcf1779455c4453af36562cf4678690",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen2.5-vl-72b-instruct",
        proxy="http://127.0.0.1:26561",  # 使用代理
        omml=omml
    )

    print(latex)
