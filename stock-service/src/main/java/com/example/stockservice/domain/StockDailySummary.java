package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDate;

@Entity
@Getter
public class StockDailySummary {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "code",  nullable = false)
    private String code;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "date", nullable = false)
    private LocalDate date;

    @Column(name = "open_price", nullable = false)
    private Integer openPrice;

    @Column(name = "high_price", nullable = false)
    private Integer highPrice;

    @Column(name = "low_price", nullable = false)
    private Integer lowPrice;

    @Column(name = "close_price", nullable = false)
    private Integer closePrice;

    @Column(name = "volume", nullable = false)
    private Long volume;

    @Column(name = "per", nullable = false)
    private Float per;

    @Column(name = "pbr", nullable = false)
    private Float pbr;

    @Column(name = "eps", nullable = false)
    private Integer eps;

    @Column(name = "bps", nullable = false)
    private Integer bps;

    @Column(name = "market", nullable = false)
    private String market;
}
