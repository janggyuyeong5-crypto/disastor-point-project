package com.example.demo.service;

import com.example.demo.domain.FloodShelter;
import com.example.demo.repository.FloodShelterRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class FloodShelterService {

    // 스프링이 주입해 준 리포지토리 인스턴스(객체)
    private final FloodShelterRepository floodShelterRepository;

    public List<FloodShelter> findAllFloodShelters() {
        // [수정 전] return FloodShelterRepository.indAll(); -> 대문자 클래스 호출 및 오타(indAll)
        // [수정 후] 주입받은 객체 변수명(소문자)과 정확한 메서드명(findAll) 사용
        return floodShelterRepository.findAll();
    }

    public FloodShelter findShelterById(Long id) {
        // [수정 전] return (FloodShelter) floodShelterRepository.findById(id)... -> 불필요한 캐스팅
        // [수정 후] Optional이 unpack되면서 바로 FloodShelter 객체가 반환됨
        return floodShelterRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("해당 ID의 대피소가 존재하지 않습니다: " + id));
    }
}