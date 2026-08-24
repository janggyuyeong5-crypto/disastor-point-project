package com.example.demo.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter @Setter
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // 게시글 고유 번호 (PK)

    private String title;   // 글 제목

    @Column(length = 1000)
    private String content; // 글 내용 (길게 쓸 수 있도록 설정)
    private String writer; // 🟢 작성자(유저 아이디) 필드 추가
}