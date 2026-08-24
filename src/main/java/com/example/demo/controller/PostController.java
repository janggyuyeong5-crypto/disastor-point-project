package com.example.demo.controller;

import com.example.demo.domain.Post;
import com.example.demo.dto.PostCreateDto;
import com.example.demo.service.PostService;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class PostController {

    private final PostService postService;

    // 1. 게시글 목록 페이지
    @GetMapping("/posts")
    public String listPosts(Model model) {
        List<Post> posts = postService.getAllPosts();
        model.addAttribute("postList", posts);
        return "list";
    }

    // 2. 글 등록 처리 (로그인한 유저 아이디를 함께 넘김)
    @PostMapping("/api/posts")
    public String createPost(PostCreateDto dto, HttpSession session) {
        String loginUser = (String) session.getAttribute("loginUser");
        if (loginUser == null) {
            return "redirect:/login";
        }
        postService.createPost(dto, loginUser);
        return "redirect:/posts";
    }

    // 3. 상세보기 페이지
    @GetMapping("/posts/{id}")
    public String detailPost(@PathVariable("id") Long id, Model model) {
        Post post = postService.getPostById(id);
        model.addAttribute("post", post);
        return "detail";
    }

    // 4. 글 삭제 처리 (본인 글만 삭제 가능하도록 보안 체크)
    @PostMapping("/posts/delete/{id}")
    public String deletePost(@PathVariable("id") Long id, HttpSession session) {
        String loginUser = (String) session.getAttribute("loginUser");
        Post post = postService.getPostById(id);

        // 현재 로그인한 사람과 글 작성자가 같을 때만 삭제 수행
        if (post.getWriter() != null && post.getWriter().equals(loginUser)) {
            postService.deletePost(id);
        }

        return "redirect:/posts";
    }
}