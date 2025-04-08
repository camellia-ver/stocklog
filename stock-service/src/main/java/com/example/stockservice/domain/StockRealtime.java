package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Table(name = "stock_realtime")
@Entity
public class StockRealtime {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "code", unique = true)
    private String code;

    @Column(name = "name")
    private String name;

    @Column(name = "price")
    private Integer price;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "market")
    private String market;

    private StockRealtime(){}

    @Builder
    public StockRealtime(String code, String name, int price,
                         LocalDateTime createdAt, String market){
        this.code = code;
        this.name = name;
        this.price = price;
        this.createdAt = createdAt;
        this.market = market;
    }
}
