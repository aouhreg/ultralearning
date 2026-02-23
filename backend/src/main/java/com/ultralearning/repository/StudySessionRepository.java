package com.ultralearning.repository;

import com.ultralearning.model.entity.StudySession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface StudySessionRepository extends JpaRepository<StudySession, Long> {
    List<StudySession> findByLearningGoalIdOrderByStartedAtDesc(Long goalId);

    @Query("SELECT s FROM StudySession s WHERE s.learningGoal.user.id = :userId ORDER BY s.startedAt DESC")
    List<StudySession> findRecentByUserId(Long userId);

    @Query("SELECT AVG(s.accuracyRate) FROM StudySession s WHERE s.learningGoal.id = :goalId")
    Double avgAccuracyByGoalId(Long goalId);
}
