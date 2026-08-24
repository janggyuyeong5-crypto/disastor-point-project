package com.example.demo.service;

import com.example.demo.domain.EarthquakeShelter;
import com.example.demo.repository.EarthquakeShelterRepository; // 올바른 Repository 임포트
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EarthquakeShelterService {

    // ❌ [오류 원인] Service 내부에서 자기 자신(Service)을 다시 주입받도록 작성되어 무한 루프 발생!
    // private final EarthquakeShelterService earthquakeShelterService;

    // ✅ [해결] Service는 DB에 접근하는 Repository를 주입받아야 합니다.
    private final EarthquakeShelterRepository earthquakeShelterRepository;

    // 대피소 전체 목록 조회
    public List<EarthquakeShelter> findAllEarthquakeShelters() {
        return earthquakeShelterRepository.findAll();
    }

    // 대피소 단건 상세 조회
    public EarthquakeShelter findShelterById(Long id) {
        return earthquakeShelterRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("해당 대피소가 존재하지 않습니다. id=" + id));
    }
}