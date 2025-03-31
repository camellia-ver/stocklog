package com.example.stockservice.api;

import com.example.stockservice.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class StcokApiController {
    private final StockService stockService;

    @GetMapping("/fetch-stock-data")
    public String fetchStockData() {
        stockService.fetchStockData(1,1);
        return "OK";
    }
}
