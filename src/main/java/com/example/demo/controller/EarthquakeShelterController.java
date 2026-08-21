//package com.example.demo.controller;
//
//import com.example.demo.service.EarthquakeShelterService;
//import org.springframework.web.bind.annotation.GetMapping;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RestController;
//
//import java.util.Map;
//
//@RestController // "이 클래스는 웹 브라우저나 외부 요청을 받아 처리하는 안내데스크(컨트롤러)야!"라고 알려줍니다.
//@RequestMapping("/api/earthquake")
//public class EarthquakeShelterController {
//
//    // 실무 작업을 처리할 주방장(Service)을 불러옵니다.
//    private final EarthquakeShelterService earthquakeShelterService;
//
//    // 생성자를 통해 서비스를 주입받습니다.
//    public EarthquakeShelterController(EarthquakeShelterService earthquakeShelterService) {
//        this.earthquakeShelterService = earthquakeShelterService;
//    }
//
//    @GetMapping("/test")
//    public Map<String, Object> testEarthquake() {
//        return Map.of("status", "success");
//    }
//
//    // 사용자가 웹 브라우저 주소창에 "http://localhost:8080/api/earthquake/fetch-shelters"라고 치고 들어오면 이 메서드가 실행됩니다.
//    @GetMapping("/fetch-shelters")
//    public String fetchAndSaveShelters() {
//        // 서비스에게 API 데이터를 가져와서 DB에 저장하라고 명령을 내립니다.
//        earthquakeShelterService.fetchAndSaveShelterData();
//
//        // 작업이 끝났다는 메시지를 웹 화면에 띄워줍니다.
//        return "지진 대피소 데이터 수집 및 DB 저장 완료!";
//    }
//}