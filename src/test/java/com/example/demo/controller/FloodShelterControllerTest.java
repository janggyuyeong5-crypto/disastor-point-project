//package com.example.demo.controller;
//
//import com.example.demo.service.FloodShelterService;
//import org.junit.jupiter.api.Assertions;
//import org.junit.jupiter.api.Test;
//
//import java.util.Map;
//
//class FloodShelterControllerTest {
//
//    @Test
//    void testFlood() {
//        // 1. 객체 생성
//        FloodShelterService service = new FloodShelterService();
//        FloodShelterController controller = new FloodShelterController(service);
//
//        // 2. 메서드 호출
//        Map<String, Object> response = controller.testFlood();
//
//        // 3. 결과 검증
//        Assertions.assertEquals("success", response.get("status"));
//    }
//}