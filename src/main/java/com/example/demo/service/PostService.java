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

    private final PostRepository postRepository;

    // 1. 글 등록 (작성자 아이디 함께 저장)
    @Transactional
    public void createPost(PostCreateDto dto, String writer) {
        Post post = new Post();
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());
        post.setWriter(writer); // 작성자 기록

        postRepository.save(post);
    }

    // 2. 전체 글 목록 조회
    public List<Post> getAllPosts() {
        return postRepository.findAll();
    }

    // 3. 단건 글 조회 (상세보기용)
    public Post getPostById(Long id) {
        return postRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 게시글입니다."));
    }

    // 4. 글 삭제
    @Transactional
    public void deletePost(Long id) {
        postRepository.deleteById(id);
    }
}