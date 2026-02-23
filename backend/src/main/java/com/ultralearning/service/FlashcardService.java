package com.ultralearning.service;

import com.ultralearning.model.entity.Flashcard;
import com.ultralearning.model.entity.LearningGoal;
import com.ultralearning.repository.FlashcardRepository;
import com.ultralearning.repository.LearningGoalRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class FlashcardService {

    private final FlashcardRepository flashcardRepository;
    private final LearningGoalRepository goalRepository;
    private final AiProxyService aiProxyService;

    @SuppressWarnings("unchecked")
    public List<Flashcard> generateAndSave(Long goalId, String content, int count) {
        LearningGoal goal = goalRepository.findById(goalId)
            .orElseThrow(() -> new RuntimeException("Goal not found"));

        Map<?, ?> req = Map.of("topic", goal.getTopic(), "content", content, "count", count);
        Map<?, ?> result = aiProxyService.post("/api/retrieval/flashcards", req);

        List<Map<String, Object>> cards = (List<Map<String, Object>>) result.get("flashcards");
        return cards.stream().map(cardData -> {
            Flashcard fc = new Flashcard();
            fc.setLearningGoal(goal);
            fc.setFront((String) cardData.get("front"));
            fc.setBack((String) cardData.get("back"));
            fc.setCardType((String) cardData.getOrDefault("type", "basic"));
            fc.setMemoryTip((String) cardData.get("memory_tip"));
            Object diff = cardData.get("difficulty");
            fc.setDifficulty(diff instanceof Number ? ((Number) diff).intValue() : 3);
            return flashcardRepository.save(fc);
        }).toList();
    }

    public List<Flashcard> getDueCards(Long goalId) {
        return flashcardRepository.findDueForReview(goalId, LocalDate.now());
    }

    public List<Flashcard> getAllCards(Long goalId) {
        return flashcardRepository.findByLearningGoalId(goalId);
    }

    public Flashcard reviewCard(Long cardId, int difficultyRating) {
        Flashcard card = flashcardRepository.findById(cardId)
            .orElseThrow(() -> new RuntimeException("Flashcard not found"));

        // SM-2 算法
        int repetitions = card.getRepetitions();
        int interval;
        if (difficultyRating < 3) {
            repetitions = 0;
            interval = 1;
        } else {
            if (repetitions == 0) interval = 1;
            else if (repetitions == 1) interval = 6;
            else {
                double easiness = Math.max(1.3, 2.5 + 0.1 - (5 - difficultyRating) * (0.08 + (5 - difficultyRating) * 0.02));
                interval = (int) Math.round(card.getIntervalDays() * easiness);
            }
            repetitions++;
        }

        card.setRepetitions(repetitions);
        card.setIntervalDays(interval);
        card.setNextReviewDate(LocalDate.now().plusDays(interval));
        card.setDifficulty(difficultyRating);
        card.setTotalReviews(card.getTotalReviews() + 1);
        if (difficultyRating >= 3) {
            card.setCorrectReviews(card.getCorrectReviews() + 1);
        }
        card.setLastReviewedAt(LocalDateTime.now());

        return flashcardRepository.save(card);
    }

    public long countDue(Long goalId) {
        return flashcardRepository.countDueForReview(goalId, LocalDate.now());
    }
}
