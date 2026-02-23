package com.ultralearning.model.dto;

import lombok.Data;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import jakarta.validation.constraints.*;

public class AuthDTO {

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RegisterRequest {
        @NotBlank
        @Size(min = 3, max = 50)
        private String username;

        @NotBlank
        @Email
        private String email;

        @NotBlank
        @Size(min = 6)
        private String password;

        private String displayName;
        private String learnerBackground;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LoginRequest {
        @NotBlank
        private String username;

        @NotBlank
        private String password;
    }

    @Data
    @AllArgsConstructor
    public static class AuthResponse {
        private String token;
        private Long userId;
        private String username;
        private String displayName;
        private String email;
    }
}
