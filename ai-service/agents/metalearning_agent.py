"""
Metalearning Agent - 元學習代理
生成學習路線圖與知識地圖，幫助學習者了解「如何學習」這門學科。
"""
import json
from .base_agent import call_claude

SYSTEM_PROMPT = """你是一位超級學習（Ultralearning）教練，專精於元學習（Metalearning）。
你的任務是幫助學習者在開始學習之前，先深入了解這門學科：
1. 概念（Concepts）：需要理解哪些核心觀念
2. 事實（Facts）：需要記住哪些具體知識點
3. 程序（Procedures）：需要練習哪些技能與步驟
4. 學習資源（Resources）：推薦的書籍、課程、網站
5. 學習策略（Strategy）：最有效的學習順序與方法

請以 JSON 格式返回結構化的知識地圖。"""


def generate_knowledge_map(topic: str, goal: str, time_available: str) -> dict:
    """生成主題的知識地圖與學習計畫。"""
    user_message = f"""
請為以下學習需求生成完整的知識地圖：

學習主題：{topic}
學習目標：{goal}
可用時間：{time_available}

請以下面的 JSON 格式返回（不要有任何額外文字）：
{{
  "topic": "主題名稱",
  "overview": "學科概述（2-3句話）",
  "estimated_weeks": 數字,
  "concepts": [
    {{"name": "概念名稱", "importance": "high/medium/low", "description": "簡短說明"}}
  ],
  "facts": [
    {{"content": "知識點", "category": "分類"}}
  ],
  "procedures": [
    {{"name": "技能名稱", "steps": ["步驟1", "步驟2"], "practice_method": "練習方式"}}
  ],
  "resources": [
    {{"type": "book/course/website", "name": "資源名稱", "description": "說明", "url": "可選"}}
  ],
  "learning_path": [
    {{"week": 1, "focus": "本週重點", "tasks": ["任務1", "任務2"]}}
  ],
  "common_mistakes": ["常見錯誤1", "常見錯誤2"]
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=4096)
    # 提取 JSON
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}


def generate_study_schedule(knowledge_map: dict, daily_hours: float) -> dict:
    """根據知識地圖生成每日學習計畫。"""
    user_message = f"""
根據以下知識地圖，生成詳細的每日學習計畫：

知識地圖：{json.dumps(knowledge_map, ensure_ascii=False)}
每日可用時間：{daily_hours} 小時

請返回 JSON 格式的每日計畫：
{{
  "daily_schedule": [
    {{
      "day": 1,
      "date_offset": "第1天",
      "morning": {{"duration_minutes": 30, "activity": "活動描述", "technique": "使用的學習技術"}},
      "afternoon": {{"duration_minutes": 60, "activity": "活動描述", "technique": "使用的學習技術"}},
      "evening": {{"duration_minutes": 30, "activity": "複習", "technique": "間隔重複"}}
    }}
  ],
  "weekly_review": "每週回顧建議",
  "progress_metrics": ["衡量進度的指標1", "指標2"]
}}
"""
    result = call_claude(SYSTEM_PROMPT, user_message, max_tokens=3000)
    try:
        start = result.find("{")
        end = result.rfind("}") + 1
        return json.loads(result[start:end])
    except Exception:
        return {"error": "解析失敗", "raw": result}
