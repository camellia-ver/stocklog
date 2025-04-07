package com.example.stockservice.model;

import lombok.*;

import java.time.LocalDateTime;

@Data
public class StockDTO {
    private String code;
    private String name;
    private Long price;
    private LocalDateTime createAt;
}
