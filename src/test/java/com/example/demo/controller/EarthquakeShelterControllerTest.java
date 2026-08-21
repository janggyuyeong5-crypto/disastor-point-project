//package com.example.demo.controller;
//
//import com.example.demo.repository.EarthquakeShelterRepository;
//import com.example.demo.service.EarthquakeShelterService;
//import org.junit.jupiter.api.Assertions;
//import org.junit.jupiter.api.Test;
//import org.mockito.Mockito;
//
//import java.util.Map;
//
//class EarthquakeShelterControllerTest {
//
//    @Test
//    void testEarthquake() {
//        // 1. Repository 모킹 후 서비스 및 컨트롤러 객체 생성
//        EarthquakeShelterRepository repository = Mockito.mock(EarthquakeShelterRepository.class);
//        EarthquakeShelterService service = new EarthquakeShelterService(repository);
//        EarthquakeShelterController controller = new EarthquakeShelterController(service);
//
//        // 2. 메서드 직접 호출
//        Map<String, Object> response = controller.testEarthquake();
//
//        // 3. 반환값의 status가 "success"인지 확인
//        Assertions.assertEquals("success", response.get("status"));
//    }
//}