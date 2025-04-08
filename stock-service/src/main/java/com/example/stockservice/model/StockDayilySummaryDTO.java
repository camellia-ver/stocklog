package com.example.stockservice.model;

import lombok.*;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class StockDayilySummaryDTO {
    private String code;
    private String name;
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
    private String market;
}
