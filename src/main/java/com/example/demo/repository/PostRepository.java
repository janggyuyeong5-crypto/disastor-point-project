package com.example.demo.repository;

import com.example.demo.domain.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {
    // 따로 코드를 적지 않아도, JpaRepository를 상속받는 순간
    // 데이터베이스 저장(save), 조회(findAll, findById) 등의 기능이 마법처럼 활성화됩니다!
}