package com.example.demo.repository;

import com.example.demo.domain.AirRaidShelter;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

// 1. Spring Data JPA의 Repository 인터페이스임을 명시합니다.
@Repository
// 2. JpaRepository<엔티티 타입, 기본키 타입>을 상속받아 findAll(), findById() 등 기본 SQL 메서드를 자동 생성합니다.
public interface AirRaidShelterRepository extends JpaRepository<AirRaidShelter, Long> {
    // 기본 전체 조회는 추가 메서드 선언 없이 JpaRepository의 findAll()로 즉시 사용 가능합니다.
}