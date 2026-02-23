"""
Intuition Agent - 直覺培養代理
使用費曼技巧、類比思維，幫助學習者真正理解而非記憶。
"""
import json
from .base_agent import call_claude, call_claude_stream

SYSTEM_PROMPT = """你是一位擅長深度理解的學習導師，運用費曼技巧（Feynman Technique）和類比思維：
1. 用簡單語言解釋複雜概念（如同對10歲孩子解釋）
2. 找到直觀的類比和比喻
3. 指出概念的本質和核心
4. 通過實際例子建立直覺
5. 揭示「為什麼」而不只是「是什麼」

你的目標是讓學習者真正「懂了」，而不只是記住了。"""


def explain_with_feynman(concept: str, topic: str, current_understanding: str = "") -> dict:
    """使用費曼技巧解釋概念。"""
    understanding_context = f"\n學習者當前理解：{current_understanding}" if current_understanding else ""
    user_message = f"""
請用費曼技巧解釋以下概念：

學習主題：{topic}
概念：{concept}{understanding_context}

請返回 JSON 格式：
{{
  "simple_explanation": "用最簡單的語言解釋（假設對方完全不懂）",
  "core_essence": "這個概念的本質是什麼（一句話）",
  "analogies": [
    {{"analogy": "類比描述", "similarity": "相似之處", "difference": "不同之處"}}
  ],
  "real_world_examples": ["實際例子1", "例子2"],
  "why_it_matters": "為什麼這個概念重要",
  "common_misconceptions": ["常見誤解1", "誤解2"],
  "intuition_builder": "建立直覺的思維練習",
  "deeper_questions": ["引發更深思考的問題1", "問題2"],
  "mental_model": "可以用什麼心智模型來理解"
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=3000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}


def feynman_teaching_session(concept: str, user_explanation: str):
    """學習者嘗試用自己的話解釋，AI 指出問題（流式）。"""
    user_message = f"""
學習者嘗試用費曼技巧解釋「{concept}」，請評估並指導：

學習者的解釋：
{user_explanation}

請：
1. 肯定解釋中正確的部分
2. 指出不清楚或錯誤的地方（具體指出哪裡）
3. 補充遺漏的關鍵點
4. 給出更好的表達方式
5. 提出一個能測試真正理解的問題

語氣要像蘇格拉底式對話，引導學習者自己發現問題。
"""
    for chunk in call_claude_stream(SYSTEM_PROMPT, user_message, max_tokens=2048):
        yield chunk


def generate_analogies(concept: str, learner_background: str) -> dict:
    """根據學習者背景生成個性化類比。"""
    user_message = f"""
為以下概念生成個性化類比，考慮學習者的背景：

概念：{concept}
學習者背景/興趣：{learner_background}

請返回 JSON 格式：
{{
  "personalized_analogies": [
    {{
      "domain": "類比來源領域",
      "analogy": "詳細類比描述",
      "mapping": {{"概念A": "類比中的A", "概念B": "類比中的B"}},
      "limitations": "這個類比的局限性"
    }}
  ],
  "visualization": "如何在腦海中可視化這個概念",
  "story": "用故事形式解釋的版本"
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=2000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}
