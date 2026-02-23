"""
base_agent.py — 統一 LLM 調用層
支持兩種後端，透過環境變數切換：
  LLM_PROVIDER=claude   → Anthropic Claude API
  LLM_PROVIDER=ollama   → 本地 Ollama (OpenAI-compatible)
"""
import os
import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ── 提供者選擇 ─────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude").lower()

# ── Claude 客戶端 ──────────────────────────────────────────
_claude_client = None
CLAUDE_MODEL = os.getenv("MODEL_ID", "claude-sonnet-4-6")

# ── Ollama 客戶端（使用 OpenAI 兼容 API）─────────────────
_ollama_client = None
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")


def _get_claude():
    global _claude_client
    if _claude_client is None:
        _claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _claude_client


def _get_ollama():
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OpenAI(
            base_url=f"{OLLAMA_BASE_URL}/v1",
            api_key="ollama",  # Ollama 不需要真實 key，但欄位必填
        )
    return _ollama_client


# ── 統一調用介面 ───────────────────────────────────────────

def call_claude(system_prompt: str, user_message: str, max_tokens: int = 2048) -> str:
    """非流式 LLM 調用，自動路由到對應後端。"""
    if LLM_PROVIDER == "ollama":
        return _ollama_call(system_prompt, user_message, max_tokens)
    return _claude_call(system_prompt, user_message, max_tokens)


def call_claude_stream(system_prompt: str, user_message: str, max_tokens: int = 2048):
    """流式 LLM 調用（生成器），自動路由到對應後端。"""
    if LLM_PROVIDER == "ollama":
        yield from _ollama_stream(system_prompt, user_message, max_tokens)
    else:
        yield from _claude_stream(system_prompt, user_message, max_tokens)


# ── Claude 實現 ────────────────────────────────────────────

def _claude_call(system_prompt: str, user_message: str, max_tokens: int) -> str:
    client = _get_claude()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def _claude_stream(system_prompt: str, user_message: str, max_tokens: int):
    client = _get_claude()
    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text


# ── Ollama 實現 ────────────────────────────────────────────

def _ollama_call(system_prompt: str, user_message: str, max_tokens: int) -> str:
    client = _get_ollama()
    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def _ollama_stream(system_prompt: str, user_message: str, max_tokens: int):
    client = _get_ollama()
    stream = client.chat.completions.create(
        model=OLLAMA_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ── 健康檢查 ───────────────────────────────────────────────

def get_provider_info() -> dict:
    """返回當前使用的提供者資訊（用於 /health 端點）。"""
    if LLM_PROVIDER == "ollama":
        return {"provider": "ollama", "model": OLLAMA_MODEL, "base_url": OLLAMA_BASE_URL}
    return {"provider": "claude", "model": CLAUDE_MODEL}
