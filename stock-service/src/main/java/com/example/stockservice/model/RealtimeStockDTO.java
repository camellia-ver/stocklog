package com.example.stockservice.model;

import com.example.stockservice.domain.Stock;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class RealtimeStockDTO {
    private Integer price;
    private LocalDateTime createdAt;
    private Stock stock;
}
