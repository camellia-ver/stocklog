package com.example.stockservice.service;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.repository.StockRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class StockService {
    private final StockRepository stockRepository;

    public List<Stock> searchStocksByKeyword(String keyword){
        return stockRepository.findByitmsNmContainingIgnoreCase(keyword).orElse(List.of());
    }
}
