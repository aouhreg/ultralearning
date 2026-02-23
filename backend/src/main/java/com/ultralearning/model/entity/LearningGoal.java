package com.ultralearning.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "learning_goals")
@Data
@NoArgsConstructor
public class LearningGoal {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String topic;

    @Column(length = 1000)
    private String goal;

    private String timeAvailable;
    private Double dailyHours;

    @Column(columnDefinition = "TEXT")
    private String knowledgeMapJson;  // 存儲 JSON 格式的知識地圖

    @Enumerated(EnumType.STRING)
    private GoalStatus status = GoalStatus.ACTIVE;

    private Integer overallProgress = 0;  // 0-100

    private LocalDateTime createdAt = LocalDateTime.now();
    private LocalDateTime updatedAt = LocalDateTime.now();

    @OneToMany(mappedBy = "learningGoal", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<StudySession> studySessions;

    @OneToMany(mappedBy = "learningGoal", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Flashcard> flashcards;

    public enum GoalStatus {
        ACTIVE, COMPLETED, PAUSED, ABANDONED
    }
}
