//package com.example.demo.controller;
//
//import com.example.demo.service.AirRaidShelterService; // 서비스 클래스 임포트 예시
//import org.junit.jupiter.api.Test;
//import org.junit.jupiter.api.Assertions;
//import java.util.Map;
//
//class AirRaidShelterControllerTest {
//
//    @Test
//    void testAirRaid() {
//        // 1. 객체 생성
//        AirRaidShelterService service = new AirRaidShelterService();
//        AirRaidShelterController controller = new AirRaidShelterController(service);
//
//        // 2. 메서드 호출
//        Map<String, Object> response = controller.testAirRaid();
//
//        // 3. 결과 검증
//        Assertions.assertEquals("success", response.get("status"));
//    }
//}