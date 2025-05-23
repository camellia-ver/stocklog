package com.example.stockservice.domain;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDate;

@Entity
@Table(name = "dailysummarystock", uniqueConstraints = @UniqueConstraint(columnNames = {"stock_code", "date"}))
@Getter
public class DailySummaryStock {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

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

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "stock_code", nullable = false)
    @JsonBackReference
    private Stock stock;
}
