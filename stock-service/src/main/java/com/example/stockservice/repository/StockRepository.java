package com.example.stockservice.repository;

import com.example.stockservice.domain.DailySummaryStock;
import com.example.stockservice.domain.Stock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StockRepository extends JpaRepository<DailySummaryStock, Long> {
    Optional<Stock> findByCode(String code);
    Optional<List<DailySummaryStock>> findByNameContainingIgnoreCase(String keyword);
}
