package com.example.demo.controller;

import com.example.demo.domain.FloodShelter;
import com.example.demo.service.FloodShelterService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController // 이 클래스가 REST API 요청을 처리하고 JSON을 반환하는 컨트롤러임을 선언합니다.
@RequestMapping("/api/shelters/flood") // 이 컨트롤러의 기본 URL 주소를 지정합니다. (수해 대피소 전용)
@RequiredArgsConstructor // final로 선언된 Service 객체의 생성자를 롬복이 자동으로 만들어 줍니다.
@CrossOrigin(origins = "*") // 외부 프론트엔드 앱에서 API를 호출할 때 CORS(출처 차단) 문제를 방지합니다.
public class FloodShelterController {

    private final FloodShelterService floodShelterService; // 수해 대피소 비즈니스 로직을 처리할 서비스 주입

    // GET /api/shelters/flood 요청 시 수해 대피소 전체 목록을 JSON으로 반환
    @GetMapping
    public ResponseEntity<List<FloodShelter>> getAllFloodShelters() {
        List<FloodShelter> shelters = floodShelterService.findAllFloodShelters();
        return ResponseEntity.ok(shelters); // 200 OK 상태 코드와 함께 리스트 반환
    }

    // GET /api/shelters/flood/{id} 요청 시 특정 ID의 수해 대피소 상세 정보 반환
    @GetMapping("/{id}")
    public ResponseEntity<FloodShelter> getShelterById(@PathVariable("id") Long id) {
        FloodShelter shelter = floodShelterService.findShelterById(id);
        return ResponseEntity.ok(shelter);
    }
}