package com.ultralearning.controller;

import com.ultralearning.model.dto.LearningGoalDTO;
import com.ultralearning.service.LearningGoalService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/goals")
@RequiredArgsConstructor
public class LearningGoalController {

    private final LearningGoalService goalService;

    @PostMapping
    public ResponseEntity<LearningGoalDTO.Response> createGoal(@Valid @RequestBody LearningGoalDTO.CreateRequest req) {
        return ResponseEntity.ok(goalService.createGoal(req));
    }

    @GetMapping
    public ResponseEntity<List<LearningGoalDTO.Response>> getGoals() {
        return ResponseEntity.ok(goalService.getUserGoals());
    }

    @GetMapping("/{id}")
    public ResponseEntity<LearningGoalDTO.Response> getGoal(@PathVariable Long id) {
        return ResponseEntity.ok(goalService.getGoal(id));
    }

    @PutMapping("/{id}/progress")
    public ResponseEntity<LearningGoalDTO.Response> updateProgress(
            @PathVariable Long id,
            @Valid @RequestBody LearningGoalDTO.UpdateProgressRequest req) {
        return ResponseEntity.ok(goalService.updateProgress(id, req.getProgress()));
    }
}
