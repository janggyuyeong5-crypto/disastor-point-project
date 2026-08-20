package com.example.demo.dto;

import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class PostCreateDto {
    private String title;   // 화면에서 넘어오는 제목
    private String content; // 화면에서 넘어오는 내용
}