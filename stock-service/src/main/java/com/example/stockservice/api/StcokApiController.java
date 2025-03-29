package com.example.stockservice.api;

import com.example.stockservice.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.DefaultUriBuilderFactory;

@RestController
@RequiredArgsConstructor
public class StcokApiController {
    private final StockService stockService;

    @GetMapping("/fetch-stock-data")
    public String fetchStockData() {
        stockService.fetchStockData();
        return "주식 데이터가 콘솔에 출력되었습니다.";
    }
}
