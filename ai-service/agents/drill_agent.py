"""
Drill Agent - 直接練習代理
識別學習弱點，生成針對性練習題目，實現刻意練習。
"""
import json
from .base_agent import call_claude

SYSTEM_PROMPT = """你是一位刻意練習（Deliberate Practice）專家，擅長：
1. 識別學習者的薄弱環節
2. 設計針對性的練習題目
3. 提供漸進式難度的挑戰
4. 分析練習結果找出模式

你的目標是讓學習者在最短時間內突破瓶頸，聚焦最有價值的練習。"""


def generate_practice_questions(
    topic: str,
    subtopic: str,
    difficulty: str,
    question_type: str,
    count: int = 5
) -> dict:
    """生成針對性練習題目。"""
    user_message = f"""
請為以下需求生成練習題目：

主題：{topic}
子主題：{subtopic}
難度：{difficulty}（easy/medium/hard）
題型：{question_type}（multiple_choice/short_answer/coding/problem_solving）
數量：{count}

請返回 JSON 格式：
{{
  "questions": [
    {{
      "id": 1,
      "type": "題型",
      "question": "題目內容",
      "context": "背景資訊（可選）",
      "options": ["A. 選項1", "B. 選項2", "C. 選項3", "D. 選項4"],
      "correct_answer": "正確答案",
      "explanation": "詳細解釋",
      "key_concept": "考查的核心概念",
      "difficulty": "easy/medium/hard",
      "hints": ["提示1", "提示2"]
    }}
  ],
  "topic_summary": "本組題目涵蓋的重點",
  "weak_areas_targeted": ["針對的薄弱領域"]
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=4096)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}


def analyze_weak_points(topic: str, wrong_answers: list) -> dict:
    """分析錯題模式，找出薄弱點。"""
    user_message = f"""
分析以下錯題記錄，找出學習者的薄弱點：

學習主題：{topic}
錯誤記錄：{json.dumps(wrong_answers, ensure_ascii=False)}

請返回 JSON 格式的分析報告：
{{
  "weak_areas": [
    {{
      "area": "薄弱領域",
      "error_pattern": "錯誤模式描述",
      "frequency": 出現次數,
      "severity": "high/medium/low",
      "recommended_practice": "建議練習方式"
    }}
  ],
  "root_causes": ["根本原因1", "原因2"],
  "priority_topics": ["優先複習主題1", "主題2"],
  "improvement_plan": "改進計畫建議"
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=2000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}
