package com.example.demo.service;

import com.example.demo.domain.AirRaidShelter;
import com.example.demo.repository.AirRaidShelterRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AirRaidShelterService {

    private final AirRaidShelterRepository airRaidShelterRepository;


    public List<AirRaidShelter> findAllAirRaidShelters() {
        return airRaidShelterRepository.findAll();
    }

    public AirRaidShelter findShelterById(Long id) {
        return airRaidShelterRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("해당 ID의 대피소가 존재하지 않습니다: " + id));
    }
}