package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Getter;

import java.util.List;

@Table(name = "stock")
@Getter
@Entity
public class Stock {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @ManyToMany(mappedBy = "favoriteStocks")
    private List<User> users;

}
