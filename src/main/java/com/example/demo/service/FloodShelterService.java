package com.example.demo.service;

import com.example.demo.domain.FloodShelter;
import org.springframework.stereotype.Service;
import java.util.Collections;
import java.util.List;

@Service
public class FloodShelterService {

    //repository를 통한 db 조회 로직
    public List<FloodShelter> getAllShelters(){
        return Collections.emptyList();
    }
}
