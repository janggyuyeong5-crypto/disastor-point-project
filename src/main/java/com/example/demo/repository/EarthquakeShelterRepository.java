package com.example.demo.repository;

import com.example.demo.domain.EarthquakeShelter;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EarthquakeShelterRepository extends JpaRepository<EarthquakeShelter, Long> {
}
