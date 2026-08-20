//package com.example.demo.controller;
//
//import com.example.demo.service.EarthquakeShelterService;
//import org.junit.jupiter.api.Assertions;
//import org.junit.jupiter.api.Test;
//
//import java.util.Map;
//
//class EarthquakeShelterControllerTest {
//
//    @Test
//    void testEarthquake() {
//        // 1. 컨트롤러 객체 생성
//        EarthquakeShelterService service = new EarthquakeShelterService();
//        EarthquakeShelterController controller = new EarthquakeShelterController(service);
//
//        // 2. 메서드 직접 호출
//        Map<String, Object> response = controller.testEarthquake();
//
//        // 3. 반환값의 status가 "success"인지 확인
//        Assertions.assertEquals("success", response.get("status"));
//    }
//}