package com.example.demo.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity // 1. "이 클래스는 데이터베이스의 테이블과 1:1로 연결됩니다!"라는 명찰입니다.
@Getter
@Setter
public class User {

    @Id // 2. "이 변수가 각 회원을 구분하는 고유 번호(주민번호 같은 역할)입니다."
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 3. 번호를 1번, 2번... 자동으로 매겨달라는 뜻입니다.
    private Long id;

    private String username; // 아이디
    private String password; // 비밀번호
    private String email;    //
    private String realname;
}