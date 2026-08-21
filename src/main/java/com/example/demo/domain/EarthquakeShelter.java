package com.example.demo.domain;

import jakarta.persistence.Column;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Entity; // 1. JPA 관리 대상 엔티티 선언용
import jakarta.persistence.Table;  // 2. 실제 DB 테이블 이름 매핑용
import jakarta.persistence.Id;     // 3. PRIMARY KEY 지정용
import lombok.Data;
import java.math.BigDecimal;


@Data
@Entity
@Table(name = "earthquake")
public class EarthquakeShelter {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "shlt_id")
    private Long shlt_id;
    private String ctpv_nm;
    private String sgg_nm;
    private String fclt_nm;
    private String daddr;
    private BigDecimal lot_DECIMAL;
    private BigDecimal lat_DECIMAL;
    private String mng_dept_nm;
}
