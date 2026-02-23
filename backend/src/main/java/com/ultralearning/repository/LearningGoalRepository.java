package com.ultralearning.repository;

import com.ultralearning.model.entity.LearningGoal;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface LearningGoalRepository extends JpaRepository<LearningGoal, Long> {
    List<LearningGoal> findByUserIdOrderByCreatedAtDesc(Long userId);

    @Query("SELECT COUNT(s) FROM StudySession s WHERE s.learningGoal.id = :goalId")
    Long countSessionsByGoalId(Long goalId);

    @Query("SELECT COUNT(f) FROM Flashcard f WHERE f.learningGoal.id = :goalId")
    Long countFlashcardsByGoalId(Long goalId);
}
