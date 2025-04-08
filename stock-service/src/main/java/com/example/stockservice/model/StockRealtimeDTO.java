package com.example.stockservice.model;

import lombok.Data;

@Data
public class StockRealtimeDTO {
    private String code;
    private String name;
    private Integer price;
    private String market;
}
