package com.ultralearning.controller;

import com.ultralearning.service.AiProxyService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Proxies AI-related requests from the frontend to the Python AI service.
 * All endpoints require JWT authentication.
 */
@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiProxyService aiProxyService;

    // ── Drill ──────────────────────────────────────────────────────────────

    @PostMapping("/drill/questions")
    public ResponseEntity<?> getDrillQuestions(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/drill/questions", body));
    }

    @PostMapping("/drill/analyze-weak-points")
    public ResponseEntity<?> analyzeWeakPoints(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/drill/analyze-weak-points", body));
    }

    // ── Retrieval ──────────────────────────────────────────────────────────

    @PostMapping("/retrieval/flashcards")
    public ResponseEntity<?> generateFlashcards(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/retrieval/flashcards", body));
    }

    @PostMapping("/retrieval/recall-quiz")
    public ResponseEntity<?> recallQuiz(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/retrieval/recall-quiz", body));
    }

    // ── Feedback ───────────────────────────────────────────────────────────

    @PostMapping("/feedback/evaluate")
    public ResponseEntity<?> evaluateAnswer(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/feedback/evaluate", body));
    }

    @PostMapping("/feedback/progress")
    public ResponseEntity<?> trackProgress(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/feedback/progress", body));
    }

    // ── Intuition ──────────────────────────────────────────────────────────

    @PostMapping("/intuition/feynman-explain")
    public ResponseEntity<?> feynmanExplain(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/intuition/feynman-explain", body));
    }

    @PostMapping("/intuition/analogies")
    public ResponseEntity<?> analogies(@RequestBody Map<String, Object> body) {
        return ResponseEntity.ok(aiProxyService.post("/api/intuition/analogies", body));
    }
}
