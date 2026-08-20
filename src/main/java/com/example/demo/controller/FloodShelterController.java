package com.example.demo.controller;

// 수해 관련 도메인 및 서비스 임포트
import com.example.demo.domain.FloodShelter;
import com.example.demo.service.FloodShelterService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/flood")
public class FloodShelterController {

    private final FloodShelterService floodShelterService;

    public FloodShelterController(FloodShelterService floodShelterService) {
        this.floodShelterService = floodShelterService;
    }

    @GetMapping("/test")
    public Map<String, Object> testFlood() {
        return Map.of("status", "success");
    }

    @GetMapping("/shelters")
    public List<FloodShelter> getShelters() {
        return floodShelterService.getAllShelters();
    }
}