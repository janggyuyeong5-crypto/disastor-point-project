package com.example.demo.controller;

import com.example.demo.domain.Post;
import org.springframework.ui.Model;
import java.util.List;
import com.example.demo.dto.PostCreateDto;
import com.example.demo.service.PostService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequiredArgsConstructor
public class PostController {

    private final PostService postService; // 게시글 전담 주방장

    // 1. 게시글 목록을 보여주는 페이지 (GET /posts)
    @GetMapping("/posts")
    public String listPosts(Model model) {
        List<Post> posts = postService.getAllPosts();
        model.addAttribute("postList", posts);
        return "list"; // templates/list.html 화면을 띄움
    }

    // 2. 🟢 [통합된 글 등록 창구] 등록하기 버튼을 눌렀을 때 실행
    @PostMapping("/api/posts")
    public String createPost(PostCreateDto dto) {
        // 주방장(PostService)에게 글 저장을 지시합니다.
        // (만약 서비스에 있는 메서드 이름이 createPost라면 postService.createPost(dto);로 맞춰주세요!)
        postService.createPost(dto);

        // 등록 완료 후 게시글 목록 화면(/posts)으로 시원하게 점프!
        return "redirect:/posts";
    }
    @GetMapping("/posts/{id}")
    public String detailPost(@PathVariable("id") Long id, Model model) {
        // 주방장(PostService)에게 해당 번호의 글을 찾아오라고 시킵니다.
        Post post = postService.getPostById(id);
        model.addAttribute("post", post);
        return "detail"; // templates/detail.html 화면을 띄웁니다.
    }
}