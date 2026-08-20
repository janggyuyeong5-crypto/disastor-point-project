package com.example.demo.controller;

// 민방위 공습 관련 도메인 및 서비스 임포트
import com.example.demo.domain.AirRaidShelter;
import com.example.demo.service.AirRaidShelterService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/airraid")
public class AirRaidShelterController {

    private final AirRaidShelterService airRaidShelterService;

    public AirRaidShelterController(AirRaidShelterService airRaidShelterService) {
        this.airRaidShelterService = airRaidShelterService;
    }

    @GetMapping("/test")
    public Map<String, Object> testAirRaid() {
        return Map.of("status", "success");
    }

    @GetMapping("/shelters")
    public List<AirRaidShelter> getShelters() {
        return airRaidShelterService.getAllShelters();
    }
}