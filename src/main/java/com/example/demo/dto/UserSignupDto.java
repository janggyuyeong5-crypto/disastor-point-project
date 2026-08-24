package com.example.demo.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserSignupDto {
    private String username;
    private String password;
    private String email;
    private String realname; // 🟢 화면의 name="realname"과 정확히 일치해야 합니다!
}