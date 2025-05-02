
from http import HTTPStatus
import dashscope  # 阿里云同义千问sdk


dashscope.api_key = "sk-48febdd659b8404badee24fa6f069899"  # 阿里云同义千问api_key 

def evaluate_answer(user_answer: str,question_text: str) -> str:
    """
    使用阿里云同义千问API对用户的回答进行评价
    参数:
    user_answer (str): 用户的回答
    question_text (str): 问题的题干
    返回:
    str: 评价结果
    """
    # 构建prompt
    prompt = (
        "你是一位专业的、严格但公正的面试官。\n"
        "请根据以下面试问题和用户的回答，给出一个简洁的评价。\n"
        f"面试问题: {question_text}\n" 
        f"用户回答: {user_answer}\n"
        "请给出评价，内容包括：\n"
        "1. 评价内容\n"
        "2. 评价分数(1-10分)\n"
        "3. 评价建议\n"
    )

    try:
        # 调用阿里云同义千问API进行评价
        response = dashscope.Generation.call(
            prompt=prompt,
            model="deepseek-r1",
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9,
            frequency_penalty=0.2,
            presence_penalty=0.1,
            result_format="message",
        )
        if response.status_code == HTTPStatus.OK:
            # 解析API返回的结果
            reply = response.output.choices[0].message.content.strip()
            return reply  # 返回评价结果
        else:
            # 处理API调用失败的情况
            return f"[AI错误]：状态码 {response.status_code}，信息：{response.message}"
    except Exception as e:
        # 处理异常情况
        return f"[AI错误]:{str(e)}"







   