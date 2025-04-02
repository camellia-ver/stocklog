package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Table(name = "stock")
@Getter
@Entity
public class Stock {
    @Id
    @Column(name = "code", updatable = false)
    private String code;

    @ManyToMany(mappedBy = "favoriteStocks")
    private List<User> users;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "open", nullable = false)
    private Double open;

    @Column(name = "open", nullable = false)
    private Double high;

    @Column(name = "low", nullable = false)
    private Double low;

    @Column(name = "close", nullable = false)
    private Double close;

    @Column(name = "volume", nullable = false)
    private Long volume;

    private Stock(){}

    @Builder
    public Stock(String code, String name, Double open, Double high,
                 Double low, Double close, Long volume) {
        this.code = code;
        this.name = name;
        this.open = open;
        this.high = high;
        this.low = low;
        this.close = close;
        this.volume = volume;
    }
}
