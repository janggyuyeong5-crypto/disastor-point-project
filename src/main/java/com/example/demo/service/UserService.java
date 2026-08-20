package com.example.demo.service;

import com.example.demo.domain.User;
import com.example.demo.dto.UserSignupDto;
import com.example.demo.repository.UserRepository;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository; // 회원 장부 관리자

    // 1. 회원가입 로직
    @Transactional
    public void registerUser(UserSignupDto dto) {
        // 아이디 중복 확인
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new IllegalArgumentException("이미 존재하는 아이디입니다.");
        }

        // 새 회원 정보 저장
        User user = new User();
        user.setUsername(dto.getUsername());
        user.setPassword(dto.getPassword()); // 주의: 실제로는 반드시 암호화해야 합니다.
        user.setEmail(dto.getEmail());
        user.setRealname(dto.getRealname());

        userRepository.save(user);
    }

    // 2. 로그인 검증 로직 (중복을 제거한 깔끔한 단일 메서드)
    public User login(String username, String password) {
        // 1. DB에서 입력받은 아이디로 유저를 찾습니다. (없으면 예외 발생)
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 아이디입니다."));

        // 2. DB에 저장된 비밀번호와 입력한 비밀번호가 일치하는지 확인합니다.
        if (!user.getPassword().equals(password)) {
            throw new IllegalArgumentException("비밀번호가 일치하지 않습니다.");
        }

        // 3. 검증을 통과하면 유저 정보를 반환합니다.
        return user;
    }
}