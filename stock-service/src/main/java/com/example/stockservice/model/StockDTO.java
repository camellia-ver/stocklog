package com.example.stockservice.model;

import lombok.*;

@Data
public class StockDTO {
    private String code;
    private String name;
    private Double open;
    private Double high;
    private Double low;
    private Double close;
    private Long volume;
}
