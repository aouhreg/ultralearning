package com.ultralearning.controller;

import com.ultralearning.model.entity.Flashcard;
import com.ultralearning.service.FlashcardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/flashcards")
@RequiredArgsConstructor
public class FlashcardController {

    private final FlashcardService flashcardService;

    @PostMapping("/generate")
    public ResponseEntity<List<Flashcard>> generate(@RequestBody Map<String, Object> body) {
        Long goalId = Long.valueOf(body.get("goalId").toString());
        String content = (String) body.get("content");
        int count = body.containsKey("count") ? Integer.parseInt(body.get("count").toString()) : 10;
        return ResponseEntity.ok(flashcardService.generateAndSave(goalId, content, count));
    }

    @GetMapping("/goal/{goalId}")
    public ResponseEntity<List<Flashcard>> getAll(@PathVariable Long goalId) {
        return ResponseEntity.ok(flashcardService.getAllCards(goalId));
    }

    @GetMapping("/goal/{goalId}/due")
    public ResponseEntity<List<Flashcard>> getDue(@PathVariable Long goalId) {
        return ResponseEntity.ok(flashcardService.getDueCards(goalId));
    }

    @GetMapping("/goal/{goalId}/due-count")
    public ResponseEntity<Map<String, Long>> getDueCount(@PathVariable Long goalId) {
        return ResponseEntity.ok(Map.of("count", flashcardService.countDue(goalId)));
    }

    @PostMapping("/{id}/review")
    public ResponseEntity<Flashcard> review(@PathVariable Long id, @RequestBody Map<String, Integer> body) {
        return ResponseEntity.ok(flashcardService.reviewCard(id, body.get("difficulty_rating")));
    }
}
