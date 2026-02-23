package com.ultralearning.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ultralearning.model.dto.LearningGoalDTO;
import com.ultralearning.model.entity.LearningGoal;
import com.ultralearning.model.entity.User;
import com.ultralearning.repository.LearningGoalRepository;
import com.ultralearning.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class LearningGoalService {

    private final LearningGoalRepository goalRepository;
    private final UserRepository userRepository;
    private final AiProxyService aiProxyService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    private User getCurrentUser() {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        return userRepository.findByUsername(username)
            .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public LearningGoalDTO.Response createGoal(LearningGoalDTO.CreateRequest req) {
        User user = getCurrentUser();
        LearningGoal goal = new LearningGoal();
        goal.setUser(user);
        goal.setTopic(req.getTopic());
        goal.setGoal(req.getGoal());
        goal.setTimeAvailable(req.getTimeAvailable());
        goal.setDailyHours(req.getDailyHours());

        // 調用 AI 服務生成知識地圖
        try {
            Map<?, ?> kmRequest = Map.of(
                "topic", req.getTopic(),
                "goal", req.getGoal(),
                "time_available", req.getTimeAvailable() != null ? req.getTimeAvailable() : "3個月"
            );
            Map<?, ?> knowledgeMap = aiProxyService.post("/api/metalearning/knowledge-map", kmRequest);
            goal.setKnowledgeMapJson(objectMapper.writeValueAsString(knowledgeMap));
        } catch (Exception e) {
            goal.setKnowledgeMapJson("{}");
        }

        goal = goalRepository.save(goal);
        return toResponse(goal);
    }

    public List<LearningGoalDTO.Response> getUserGoals() {
        User user = getCurrentUser();
        return goalRepository.findByUserIdOrderByCreatedAtDesc(user.getId())
            .stream().map(this::toResponse).toList();
    }

    public LearningGoalDTO.Response getGoal(Long id) {
        LearningGoal goal = goalRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Goal not found"));
        return toResponse(goal);
    }

    public LearningGoalDTO.Response updateProgress(Long id, Integer progress) {
        LearningGoal goal = goalRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Goal not found"));
        goal.setOverallProgress(progress);
        goal.setUpdatedAt(LocalDateTime.now());
        if (progress >= 100) {
            goal.setStatus(LearningGoal.GoalStatus.COMPLETED);
        }
        return toResponse(goalRepository.save(goal));
    }

    private LearningGoalDTO.Response toResponse(LearningGoal goal) {
        LearningGoalDTO.Response res = new LearningGoalDTO.Response();
        res.setId(goal.getId());
        res.setTopic(goal.getTopic());
        res.setGoal(goal.getGoal());
        res.setTimeAvailable(goal.getTimeAvailable());
        res.setDailyHours(goal.getDailyHours());
        res.setKnowledgeMapJson(goal.getKnowledgeMapJson());
        res.setStatus(goal.getStatus());
        res.setOverallProgress(goal.getOverallProgress());
        res.setCreatedAt(goal.getCreatedAt());
        res.setUpdatedAt(goal.getUpdatedAt());
        res.setTotalSessions(goalRepository.countSessionsByGoalId(goal.getId()));
        res.setFlashcardCount(goalRepository.countFlashcardsByGoalId(goal.getId()));
        return res;
    }
}
