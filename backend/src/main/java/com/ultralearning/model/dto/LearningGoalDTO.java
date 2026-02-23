package com.ultralearning.model.dto;

import com.ultralearning.model.entity.LearningGoal;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;

public class LearningGoalDTO {

    @Data
    @NoArgsConstructor
    public static class CreateRequest {
        @NotBlank
        private String topic;

        @NotBlank
        private String goal;

        private String timeAvailable;
        private Double dailyHours = 1.0;
    }

    @Data
    @NoArgsConstructor
    public static class Response {
        private Long id;
        private String topic;
        private String goal;
        private String timeAvailable;
        private Double dailyHours;
        private String knowledgeMapJson;
        private LearningGoal.GoalStatus status;
        private Integer overallProgress;
        private LocalDateTime createdAt;
        private LocalDateTime updatedAt;
        private Long totalSessions;
        private Long flashcardCount;
    }

    @Data
    @NoArgsConstructor
    public static class UpdateProgressRequest {
        @NotNull
        @Min(0) @Max(100)
        private Integer progress;
    }
}
