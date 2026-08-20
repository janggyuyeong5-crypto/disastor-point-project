package com.example.demo.service;

import com.example.demo.domain.AirRaidShelter;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

@Service
public class AirRaidShelterService {

    //repository를 통한 db 조회 로직
    public List<AirRaidShelter> getAllShelters(){
        return Collections.emptyList();
    }
}
