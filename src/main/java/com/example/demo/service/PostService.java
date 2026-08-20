package com.example.demo.service;

import com.example.demo.domain.Post;
import com.example.demo.dto.PostCreateDto;
import com.example.demo.repository.PostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PostService {

    private final PostRepository postRepository; // 게시글 창고 관리자

    @Transactional
    public void createPost(PostCreateDto dto) {
        // 1. 새 게시글 장부 생성
        Post post = new Post();
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());

        // 2. 창고 관리자를 통해 데이터베이스에 저장
        postRepository.save(post);
    }
    public List<Post> getAllPosts() {
        return postRepository.findAll();
    }

    public void savePost(PostCreateDto dto) {
    }
    public Post getPostById(Long id) {
        return postRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 게시글입니다. ID: " + id));
    }
}