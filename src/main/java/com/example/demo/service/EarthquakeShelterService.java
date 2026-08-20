package com.example.demo.service;

import com.example.demo.domain.EarthquakeShelter;
import org.springframework.stereotype.Service;
import java.util.Collections;
import java.util.List;

@Service
public class EarthquakeShelterService {

    //repository를 통한 db 조회 로직
    public List<EarthquakeShelter> getAllShelters(){
        return Collections.emptyList();
    }
}
