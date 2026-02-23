package com.ultralearning.repository;

import com.ultralearning.model.entity.Flashcard;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.time.LocalDate;
import java.util.List;

public interface FlashcardRepository extends JpaRepository<Flashcard, Long> {
    List<Flashcard> findByLearningGoalId(Long goalId);

    @Query("SELECT f FROM Flashcard f WHERE f.learningGoal.id = :goalId AND f.nextReviewDate <= :today ORDER BY f.nextReviewDate ASC")
    List<Flashcard> findDueForReview(Long goalId, LocalDate today);

    @Query("SELECT COUNT(f) FROM Flashcard f WHERE f.learningGoal.id = :goalId AND f.nextReviewDate <= :today")
    Long countDueForReview(Long goalId, LocalDate today);
}
