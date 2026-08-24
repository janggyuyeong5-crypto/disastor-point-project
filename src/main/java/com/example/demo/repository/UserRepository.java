package com.example.demo.repository;


import com.example.demo.domain.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

// JpaRepository<보관할엔티티, 고유번호의데이터타입> 을 상속받으면, 스프링부트가 캐비닛을 자동 완성해 줍니다.
public interface UserRepository extends JpaRepository<User, Long> {

    // 캐비닛 관리자에게 내리는 특별 주문서들 (이름만 지어주면 스프링이 SQL을 알아서 짭니다)
    boolean existsByUsername(String username); // "이 아이디 가진 사람 있어?"
    Optional<User> findByUsername(String username); // "이 아이디 가진 사람 찾아와봐"
}