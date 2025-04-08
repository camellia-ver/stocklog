package com.example.stockservice.service;

import com.example.stockservice.domain.StockDailySummary;
import com.example.stockservice.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class StockService {
    private final StockRepository stockRepository;

    public List<StockDailySummary> searchStocksByKeyword(String keyword){
        return stockRepository.findByNameContainingIgnoreCase(keyword).orElse(List.of());
    }
}
