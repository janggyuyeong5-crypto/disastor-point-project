package com.example.demo.controller;

import com.example.demo.dto.UserSignupDto;
import com.example.demo.service.UserService;
import com.example.demo.domain.User; // 본인의 엔티티 패키지 경로 확인
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import jakarta.servlet.http.HttpSession;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // 1. 회원가입 처리
    @PostMapping("/api/users/signup")
    public String signup(UserSignupDto dto) {
        userService.registerUser(dto);
        return "redirect:/login";
    }

    // 2. 첫 화면
    @GetMapping("/")
    public String root() {
        return "login";
    }

    // 3. 로그인 페이지
    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    // 4. 회원가입 페이지
    @GetMapping("/signup")
    public String signupPage() {
        return "signup";
    }

    // 5. 게시판 작성 페이지 (로그인 검문소)
    @GetMapping("/write")
    public String writePage(HttpSession session) {
        Object loginUser = session.getAttribute("loginUser");
        if (loginUser == null) {
            return "redirect:/login";
        }
        return "write";
    }

    // 6. 🟢 [유일한 로그인 처리 창구] 아이디/비번 검증 후 통과!
    @PostMapping("/api/users/login")
    public String login(String username, String password, HttpSession session) {
        try {
            // 주방장(UserService)을 통해 DB에서 아이디/비번 일치 여부 확인
            User user = userService.login(username, password);

            // 검증 성공 시 세션에 유저 이름 저장
            session.setAttribute("loginUser", user.getUsername());

            return "redirect:/write"; // 게시판으로 점프!
        } catch (IllegalArgumentException e) {
            // 정보가 틀리면 로그인 창으로 강제 튕김 (프리패스 원천 차단)
            return "redirect:/login";
        }
    }
}