package com.example.stockservice.repository;

import com.example.stockservice.domain.StockDailySummary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StockRepository extends JpaRepository<StockDailySummary, Long> {
    Optional<StockDailySummary> findByCode(String code);
    Optional<List<StockDailySummary>> findByNameContainingIgnoreCase(String keyword);
}
