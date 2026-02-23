package com.ultralearning.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcards")
@Data
@NoArgsConstructor
public class Flashcard {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "learning_goal_id", nullable = false)
    private LearningGoal learningGoal;

    @Column(length = 1000, nullable = false)
    private String front;

    @Column(length = 2000, nullable = false)
    private String back;

    private String cardType = "basic";  // basic, cloze
    private String tags;
    private String memoryTip;

    // SM-2 間隔重複字段
    private Integer difficulty = 3;     // 1-5
    private Integer repetitions = 0;
    private Integer intervalDays = 1;
    private LocalDate nextReviewDate = LocalDate.now();

    private Integer totalReviews = 0;
    private Integer correctReviews = 0;

    private LocalDateTime createdAt = LocalDateTime.now();
    private LocalDateTime lastReviewedAt;
}
