package com.ultralearning.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "study_sessions")
@Data
@NoArgsConstructor
public class StudySession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "learning_goal_id", nullable = false)
    private LearningGoal learningGoal;

    @Enumerated(EnumType.STRING)
    private SessionType sessionType;  // DRILL, RETRIEVAL, INTUITION

    private String subtopic;
    private Integer totalQuestions;
    private Integer correctAnswers;
    private Double accuracyRate;
    private Integer durationMinutes;

    @Column(columnDefinition = "TEXT")
    private String resultsJson;  // 詳細結果 JSON

    @Column(columnDefinition = "TEXT")
    private String feedbackJson;  // AI 反饋 JSON

    @Enumerated(EnumType.STRING)
    private MasteryLevel masteryLevel;

    private LocalDateTime startedAt = LocalDateTime.now();
    private LocalDateTime completedAt;

    public enum SessionType {
        DRILL, RETRIEVAL, INTUITION, FEYNMAN
    }

    public enum MasteryLevel {
        BEGINNER, DEVELOPING, PROFICIENT, ADVANCED, EXPERT
    }
}
