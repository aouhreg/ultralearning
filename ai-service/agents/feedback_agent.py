"""
Feedback Agent - 即時反饋代理
評估學習者的回答，提供精準、建設性的反饋。
"""
import json
from .base_agent import call_claude, call_claude_stream

SYSTEM_PROMPT = """你是一位嚴格但鼓勵的學習教練，擅長提供高質量的學習反饋：
1. 準確評估答案的正確性和完整性
2. 指出具體的錯誤和遺漏之處
3. 解釋正確概念，糾正誤解
4. 給出改進建議和下一步學習方向
5. 保持積極鼓勵的語氣，增強學習動力

你的反饋應該具體、可操作，幫助學習者真正理解，而不只是知道答案。"""


def evaluate_answer(question: str, correct_answer: str, user_answer: str, topic: str) -> dict:
    """評估學習者的回答並提供詳細反饋。"""
    user_message = f"""
請評估以下學習者的回答：

主題：{topic}
問題：{question}
標準答案：{correct_answer}
學習者回答：{user_answer}

請返回 JSON 格式的評估結果：
{{
  "score": 0-100的分數,
  "is_correct": true/false,
  "correctness_level": "completely_correct/mostly_correct/partially_correct/incorrect",
  "feedback": {{
    "positive": "做得好的地方",
    "corrections": ["需要糾正的點1", "需要糾正的點2"],
    "missing_points": ["遺漏的重要點"],
    "misconceptions": ["需要糾正的誤解"]
  }},
  "explanation": "詳細解釋正確答案",
  "improvement_suggestions": ["改進建議1", "建議2"],
  "related_concepts": ["相關概念，建議進一步學習"],
  "encouragement": "鼓勵性的話語",
  "next_action": "建議的下一步學習行動"
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=2048)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}


def evaluate_essay_answer(question: str, user_answer: str, topic: str, rubric: dict = None):
    """評估開放式問答，流式返回反饋。"""
    rubric_text = f"\n評分標準：{json.dumps(rubric, ensure_ascii=False)}" if rubric else ""
    user_message = f"""
請評估以下開放式問答：

主題：{topic}
問題：{question}{rubric_text}
學習者回答：{user_answer}

請提供詳細的評估反饋，包括：
1. 整體評分與評級
2. 優點（具體指出）
3. 不足之處（具體指出）
4. 概念準確性分析
5. 改進建議
6. 示範更好的回答方向
"""
    for chunk in call_claude_stream(SYSTEM_PROMPT, user_message, max_tokens=2048):
        yield chunk


def track_learning_progress(topic: str, session_results: list) -> dict:
    """分析一次學習會話的整體進度。"""
    user_message = f"""
分析以下學習會話的結果，提供整體進度評估：

學習主題：{topic}
會話結果：{json.dumps(session_results, ensure_ascii=False)}

請返回 JSON 格式的進度報告：
{{
  "session_summary": {{
    "total_questions": 總題數,
    "correct_count": 正確數,
    "accuracy_rate": 準確率百分比,
    "time_spent_minutes": 時間（分鐘）
  }},
  "mastery_level": "beginner/developing/proficient/advanced/expert",
  "strong_areas": ["掌握良好的領域"],
  "weak_areas": ["需要加強的領域"],
  "trend": "improving/stable/declining",
  "recommendations": ["學習建議1", "建議2"],
  "next_session_focus": "下次學習重點",
  "estimated_mastery_date": "預計掌握時間"
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=2000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}
