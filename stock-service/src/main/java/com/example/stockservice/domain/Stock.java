package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
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

    @Column(name = "price", nullable = false)
    private Long price;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createAt;

    private Stock(){}

    @Builder
    public Stock(String code, String name, Long price, LocalDateTime createAt) {
        this.code = code;
        this.name = name;
        this.price = price;
        this.createAt = createAt;
    }
}
