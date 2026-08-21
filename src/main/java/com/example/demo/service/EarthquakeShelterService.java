//package com.example.demo.service;
//
//import com.example.demo.domain.EarthquakeShelter;
//import com.example.demo.repository.EarthquakeShelterRepository;
//
//import org.springframework.stereotype.Service;
//import org.springframework.web.client.RestTemplate;
//
//import tools.jackson.databind.JsonNode;
//import tools.jackson.databind.json.JsonMapper;
//
//import java.util.ArrayList;
//import java.util.List;
//
//@Service
//public class EarthquakeShelterService {
//
//    private final EarthquakeShelterRepository earthquakeShelterRepository;
//
//    public EarthquakeShelterService(EarthquakeShelterRepository earthquakeShelterRepository) {
//        this.earthquakeShelterRepository = earthquakeShelterRepository;
//    }
//
//    public void fetchAndSaveShelterData() {
//
//        try {
//
//            String baseUrl =
//                    "http://openapi.seoul.go.kr:8088/444e4569696568643536476365704c/json/TbEqkShelter/";
//
//            RestTemplate restTemplate = new RestTemplate();
//
//            JsonMapper jsonMapper =
//                    JsonMapper.builder().build();
//
//            List<EarthquakeShelter> shelters =
//                    new ArrayList<>();
//
//
//            // =========================
//            // 1~1000
//            // =========================
//
//            String url1 = baseUrl + "1/1000/";
//
//            String response1 =
//                    restTemplate.getForObject(url1, String.class);
//
//            JsonNode root1 =
//                    jsonMapper.readTree(response1);
//
//            JsonNode row1 =
//                    root1.path("TbEqkShelter").path("row");
//
//            if (row1.isArray()) {
//
//                for (JsonNode node : row1) {
//
//                    EarthquakeShelter shelter =
//                            createShelter(node);
//
//                    shelters.add(shelter);
//                }
//            }
//
//            System.out.println(
//                    "1~1000 데이터 가져오기 완료 : "
//                            + row1.size() + "개"
//            );
//
//
//            // =========================
//            // 1001~1551
//            // =========================
//
//            String url2 = baseUrl + "1001/1551/";
//
//            String response2 =
//                    restTemplate.getForObject(url2, String.class);
//
//            JsonNode root2 =
//                    jsonMapper.readTree(response2);
//
//            JsonNode row2 =
//                    root2.path("TbEqkShelter").path("row");
//
//            if (row2.isArray()) {
//
//                for (JsonNode node : row2) {
//
//                    EarthquakeShelter shelter =
//                            createShelter(node);
//
//                    shelters.add(shelter);
//                }
//            }
//
//            System.out.println(
//                    "1001~1551 데이터 가져오기 완료 : "
//                            + row2.size() + "개"
//            );
//
//
//            // =========================
//            // DB 저장
//            // =========================
//
//            System.out.println(
//                    "API에서 가져온 전체 데이터 : "
//                            + shelters.size() + "개"
//            );
//
//            // 기존 데이터 삭제
//            earthquakeShelterRepository.deleteAll();
//
//            // 전체 데이터 저장
//            earthquakeShelterRepository.saveAll(shelters);
//
//            System.out.println(
//                    "DB 저장 완료 : "
//                            + shelters.size() + "개"
//            );
//
//        } catch (Exception e) {
//
//            e.printStackTrace();
//        }
//    }
//
//
//    // JSON → EarthquakeShelter 변환
//    private EarthquakeShelter createShelter(JsonNode node) {
//
//        EarthquakeShelter shelter =
//                new EarthquakeShelter();
//
//        shelter.setShltId(
//                node.path("SHLT_ID").asText()
//        );
//
//        shelter.setCtpvNm(
//                node.path("CTPV_NM").asText()
//        );
//
//        shelter.setSggNm(
//                node.path("SGG_NM").asText()
//        );
//
//        shelter.setFcltNm(
//                node.path("FCLT_NM").asText()
//        );
//
//        shelter.setDaddr(
//                node.path("DADDR").asText()
//        );
//
//        shelter.setFcar(
//                node.path("FCAR").asDouble()
//        );
//
//        shelter.setLot(
//                node.path("LOT").asDouble()
//        );
//
//        shelter.setLat(
//                node.path("LAT").asDouble()
//        );
//
//        shelter.setSe(
//                node.path("SE").asText()
//        );
//
//        shelter.setSeNm(
//                node.path("SE_NM").asText()
//        );
//
//        shelter.setMngDeptNm(
//                node.path("MNG_DEPT_NM").asText()
//        );
//
//        return shelter;
//    }
//}