package com.example.stockservice.model;

import com.example.stockservice.domain.Stock;
import lombok.*;

import java.time.LocalDate;

@Data
public class DailySummaryStockDTO {
    private String code;
    private String name;
    private String market;
    private LocalDate date;
    private Integer openPrice;
    private Integer highPrice;
    private Integer lowPrice;
    private Integer closePrice;
    private Long volume;
    private Float per;
    private Float pbr;
    private Integer eps;
    private Integer bps;
    private Stock stock;
}
