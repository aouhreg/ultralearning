package com.ultralearning.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class AiProxyService {

    @Value("${ai-service.base-url}")
    private String aiServiceBaseUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public Map<?, ?> post(String path, Object requestBody) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);
        ResponseEntity<Map> response = restTemplate.exchange(
            aiServiceBaseUrl + path, HttpMethod.POST, entity, Map.class
        );
        return response.getBody();
    }

    public String postForString(String path, Object requestBody) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);
        ResponseEntity<String> response = restTemplate.exchange(
            aiServiceBaseUrl + path, HttpMethod.POST, entity, String.class
        );
        return response.getBody();
    }
}
