package com.example.demo.controller;

import com.example.demo.domain.AirRaidShelter;
import com.example.demo.service.AirRaidShelterService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// 1. 반환 데이터를 HTML 뷰가 아닌 JSON 형식의 HTTP 응답 본문(Body)으로 전송합니다.
@RestController
// 2. 이 컨트롤러에서 처리할 공통 기본 URL 경로를 지정합니다.
@RequestMapping("/api/shelters/air")
// 3. final 필드인 Service의 생성자 주입 코드를 롬복으로 자동 완성합니다.
@RequiredArgsConstructor
// 4. 프론트엔드(HTML/JS)와의 통신 시 브라우저의 CORS 정책 차단을 방지합니다.
@CrossOrigin(origins = "*")
public class AirRaidShelterController {

    // 5. 비즈니스 로직을 호출할 Service 객체를 선언합니다.
    private final AirRaidShelterService airRaidShelterService;

    /**
     * GET 요청 시 공습 대피소 전체 목록을 JSON 형태로 응답합니다.
     * 호출 URL: http://localhost:8080/api/shelters/air
     */
    @GetMapping
    public ResponseEntity<List<AirRaidShelter>> getAllAirRaidShelters() {
        // Service로부터 대피소 리스트를 받아옵니다.
        List<AirRaidShelter> shelters = airRaidShelterService.findAllAirRaidShelters();
        // 200 OK 상태 코드와 함께 JSON 리스트를 반환합니다.
        return ResponseEntity.ok(shelters);
    }

    /**
     * GET 요청 시 특정 대피소 1개의 상세 정보를 JSON 형태로 응답합니다.
     * 호출 URL 예시: http://localhost:8080/api/shelters/air/1
     */
    @GetMapping("/{id}")
    public ResponseEntity<AirRaidShelter> getShelterById(@PathVariable("id") Long id) {
        AirRaidShelter shelter = airRaidShelterService.findShelterById(id);
        return ResponseEntity.ok(shelter);
    }
}