package com.example.demo.controller;

import com.example.demo.service.AirRaidShelterService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AirRaidShelterController.class)
class AirRaidShelterControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private AirRaidShelterService airRaidShelterService;

    @Test
    @DisplayName("공습 대피소 전체 목록 API 정상 응답 테스트")
    void getAllAirRaidSheltersTest() throws Exception {
        mockMvc.perform(get("/api/shelters/air"))
                .andExpect(status().isOk());
    }
}