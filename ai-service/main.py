"""
Ultralearning AI Service - FastAPI Main Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json

from agents import (
    generate_knowledge_map, generate_study_schedule,
    generate_practice_questions, analyze_weak_points,
    generate_flashcards, calculate_next_review, generate_recall_quiz,
    evaluate_answer, evaluate_essay_answer, track_learning_progress,
    explain_with_feynman, feynman_teaching_session, generate_analogies,
)
from agents.base_agent import get_provider_info

app = FastAPI(title="Ultralearning AI Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Models ────────────────────────────────────────────────

class KnowledgeMapRequest(BaseModel):
    topic: str
    goal: str
    time_available: str

class StudyScheduleRequest(BaseModel):
    knowledge_map: dict
    daily_hours: float

class PracticeQuestionsRequest(BaseModel):
    topic: str
    subtopic: str
    difficulty: str = "medium"
    question_type: str = "multiple_choice"
    count: int = 5

class WeakPointsRequest(BaseModel):
    topic: str
    wrong_answers: List[dict]

class FlashcardsRequest(BaseModel):
    topic: str
    content: str
    count: int = 10

class ReviewScheduleRequest(BaseModel):
    card_id: int
    difficulty_rating: int
    repetitions: int
    last_interval: int

class RecallQuizRequest(BaseModel):
    topic: str
    flashcards: List[dict]

class EvaluateAnswerRequest(BaseModel):
    question: str
    correct_answer: str
    user_answer: str
    topic: str

class EssayEvaluateRequest(BaseModel):
    question: str
    user_answer: str
    topic: str
    rubric: Optional[dict] = None

class ProgressRequest(BaseModel):
    topic: str
    session_results: List[dict]

class FeynmanRequest(BaseModel):
    concept: str
    topic: str
    current_understanding: Optional[str] = ""

class FeynmanTeachRequest(BaseModel):
    concept: str
    user_explanation: str

class AnalogyRequest(BaseModel):
    concept: str
    learner_background: str


# ─── Health Check ──────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ultralearning-ai", **get_provider_info()}


# ─── Metalearning Endpoints ────────────────────────────────────────

@app.post("/api/metalearning/knowledge-map")
def api_knowledge_map(req: KnowledgeMapRequest):
    result = generate_knowledge_map(req.topic, req.goal, req.time_available)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/metalearning/study-schedule")
def api_study_schedule(req: StudyScheduleRequest):
    result = generate_study_schedule(req.knowledge_map, req.daily_hours)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ─── Drill Endpoints ───────────────────────────────────────────────

@app.post("/api/drill/questions")
def api_practice_questions(req: PracticeQuestionsRequest):
    result = generate_practice_questions(
        req.topic, req.subtopic, req.difficulty, req.question_type, req.count
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/drill/analyze-weak-points")
def api_analyze_weak_points(req: WeakPointsRequest):
    result = analyze_weak_points(req.topic, req.wrong_answers)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ─── Retrieval Endpoints ───────────────────────────────────────────

@app.post("/api/retrieval/flashcards")
def api_flashcards(req: FlashcardsRequest):
    result = generate_flashcards(req.topic, req.content, req.count)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/retrieval/review-schedule")
def api_review_schedule(req: ReviewScheduleRequest):
    return calculate_next_review(
        req.card_id, req.difficulty_rating, req.repetitions, req.last_interval
    )

@app.post("/api/retrieval/recall-quiz")
def api_recall_quiz(req: RecallQuizRequest):
    result = generate_recall_quiz(req.topic, req.flashcards)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ─── Feedback Endpoints ────────────────────────────────────────────

@app.post("/api/feedback/evaluate")
def api_evaluate_answer(req: EvaluateAnswerRequest):
    result = evaluate_answer(req.question, req.correct_answer, req.user_answer, req.topic)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/feedback/evaluate-essay")
def api_evaluate_essay(req: EssayEvaluateRequest):
    def stream_gen():
        for chunk in evaluate_essay_answer(req.question, req.user_answer, req.topic, req.rubric):
            yield chunk
    return StreamingResponse(stream_gen(), media_type="text/plain; charset=utf-8")

@app.post("/api/feedback/progress")
def api_track_progress(req: ProgressRequest):
    result = track_learning_progress(req.topic, req.session_results)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# ─── Intuition Endpoints ───────────────────────────────────────────

@app.post("/api/intuition/feynman-explain")
def api_feynman_explain(req: FeynmanRequest):
    result = explain_with_feynman(req.concept, req.topic, req.current_understanding)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/intuition/feynman-teach")
def api_feynman_teach(req: FeynmanTeachRequest):
    def stream_gen():
        for chunk in feynman_teaching_session(req.concept, req.user_explanation):
            yield chunk
    return StreamingResponse(stream_gen(), media_type="text/plain; charset=utf-8")

@app.post("/api/intuition/analogies")
def api_analogies(req: AnalogyRequest):
    result = generate_analogies(req.concept, req.learner_background)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
