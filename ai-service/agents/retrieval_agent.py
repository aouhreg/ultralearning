"""
Retrieval Agent - 主動回憶代理
生成閃卡、測驗題，實現間隔重複和主動提取記憶。
"""
import json
from .base_agent import call_claude

SYSTEM_PROMPT = """你是一位記憶與回憶（Retrieval Practice）專家，擅長：
1. 設計高效閃卡（Flashcards）
2. 創建間隔重複學習系統
3. 運用主動回憶技術強化長期記憶
4. 設計填空、問答等各類回憶練習

你遵循 Anki/SuperMemo 的最佳實踐，創建簡潔、原子化、高效的記憶材料。"""


def generate_flashcards(topic: str, content: str, count: int = 10) -> dict:
    """從學習內容生成閃卡。"""
    user_message = f"""
請根據以下學習內容生成高質量閃卡：

主題：{topic}
學習內容：{content}
數量：{count}

閃卡設計原則：
- 每張卡片只考查一個知識點（原子性）
- 問題要清晰、具體
- 答案要簡潔但完整
- 包含記憶技巧和聯想

請返回 JSON 格式：
{{
  "flashcards": [
    {{
      "id": 1,
      "front": "問題或提示",
      "back": "答案",
      "type": "basic/cloze/image_occlusion",
      "tags": ["標籤1", "標籤2"],
      "memory_tip": "記憶技巧",
      "difficulty": 1-5,
      "next_review_days": 1
    }}
  ],
  "deck_name": "卡組名稱",
  "total_cards": 數字,
  "study_tips": ["學習建議1", "建議2"]
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=4096)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}


def calculate_next_review(card_id: int, difficulty_rating: int, repetitions: int, last_interval: int) -> dict:
    """使用 SM-2 算法計算下次複習時間。"""
    # SM-2 算法實現
    if difficulty_rating < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            easiness = max(1.3, 2.5 + 0.1 - (5 - difficulty_rating) * (0.08 + (5 - difficulty_rating) * 0.02))
            interval = round(last_interval * easiness)
        repetitions += 1

    return {
        "card_id": card_id,
        "next_interval_days": interval,
        "repetitions": repetitions,
        "difficulty_rating": difficulty_rating
    }


def generate_recall_quiz(topic: str, flashcards: list) -> dict:
    """從閃卡生成綜合測驗。"""
    cards_text = json.dumps(flashcards[:10], ensure_ascii=False)
    user_message = f"""
根據以下閃卡內容，生成一套綜合回憶測驗：

主題：{topic}
閃卡內容：{cards_text}

請返回 JSON 格式的測驗：
{{
  "quiz_title": "測驗標題",
  "questions": [
    {{
      "id": 1,
      "type": "recall/multiple_choice/true_false/fill_blank",
      "question": "問題",
      "answer": "答案",
      "options": ["選項（僅多選題）"],
      "source_card_id": 相關閃卡ID
    }}
  ],
  "time_limit_minutes": 估計時間,
  "passing_score": 及格分數百分比
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=3000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}
