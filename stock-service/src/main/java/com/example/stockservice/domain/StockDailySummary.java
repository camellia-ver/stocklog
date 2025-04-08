package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;

import java.time.LocalDate;

@Table(name = "stock_daily_summary")
@Entity
public class StockDailySummary {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "code", unique = true)
    private String code;

    @Column(name = "name")
    private String name;

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "open_price")
    private Integer openPrice;

    @Column(name = "high_price")
    private Integer highPrice;

    @Column(name = "low_price")
    private Integer lowPrice;

    @Column(name = "close_price")
    private Integer closePrice;

    @Column(name = "volume")
    private Long volume;

    @Column(name = "per")
    private Float per;

    @Column(name = "pbr")
    private Float pbr;

    @Column(name = "eps")
    private Integer eps;

    @Column(name = "bps")
    private Integer bps;

    @Column(name = "market")
    private String market;

    private StockDailySummary(){};

    @Builder
    public StockDailySummary(String code, String name, LocalDate date, Integer openPrice,
                             Integer highPrice, Integer lowPrice, Integer closePrice,
                             Long volume, Float per,Float pbr, Integer eps,
                             Integer bps, String market){
        this.code = code;
        this.name = name;
        this.date = date;
        this.openPrice = openPrice;
        this.highPrice = highPrice;
        this.lowPrice = lowPrice;
        this.closePrice = closePrice;
        this.volume = volume;
        this.per = per;
        this.pbr = pbr;
        this.eps = eps;
        this.bps = bps;
        this.market = market;
    }
}
