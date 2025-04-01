package com.example.stockservice.api;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
public class StcokApiController {
    private final StockService stockService;

    @GetMapping("/stocks/search")
    public List<Stock> searchStocks(@RequestParam String keyword){
        return stockService.searchStocksByKeyword(keyword);
    }
}
