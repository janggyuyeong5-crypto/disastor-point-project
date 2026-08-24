package com.example.demo.controller;

import com.example.demo.domain.User;
import com.example.demo.dto.UserSignupDto;
import com.example.demo.service.UserService;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/")
    public String root() {
        return "login";
    }

    @GetMapping("/login")
    public String loginPage() {
        return "login";
    }

    @GetMapping("/signup")
    public String signupPage() {
        return "signup";
    }

    @GetMapping("/write")
    public String writePage(HttpSession session) {
        Object loginUser = session.getAttribute("loginUser");
        if (loginUser == null) {
            return "redirect:/login";
        }
        return "write";
    }

    // 🟢 [핵심 수정] 로그인 처리 창구
    @PostMapping("/api/users/login")
    public String login(String username, String password, HttpSession session, Model model) {
        try {
            User user = userService.login(username, password);
            session.setAttribute("loginUser", user.getUsername());
            return "redirect:/posts"; // 성공 시 게시판으로 이동
        } catch (IllegalArgumentException e) {
            // 정보가 틀리면 에러 메시지를 챙겨서 로그인 창을 다시 보여줍니다!
            model.addAttribute("errorMessage", "아이디 또는 비밀번호가 잘못되었습니다.");
            return "login";
        }
    }

    // 회원가입 처리 창구
    @PostMapping("/api/users/signup")
    public String signup(UserSignupDto dto, Model model) {
        try {
            userService.registerUser(dto);
            return "redirect:/login";
        } catch (IllegalArgumentException e) {
            model.addAttribute("errorMessage", e.getMessage());
            return "signup";
        }
    }
}