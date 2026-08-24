package com.example.demo.repository;

import com.example.demo.domain.FloodShelter;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

// 1. Spring Data JPA가 제공하는 JpaRepository를 상속받습니다.
// 2. <대상 엔티티 클래스, 엔티티의 Primary Key(@Id) 타입>을 지정합니다.
@Repository
public interface FloodShelterRepository extends JpaRepository<FloodShelter, Long> {
    // JpaRepository를 상속받으면 기본적인 findAll(), findById(), save() 등의 메서드를
    // 스프링이 자동으로 구현체를 만들어 빈(Bean)으로 등록해 줍니다.
}