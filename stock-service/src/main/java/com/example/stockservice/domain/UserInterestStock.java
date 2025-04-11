package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "userintereststock")
@Getter
public class UserInterestStock {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "stock_code",referencedColumnName = "code", nullable = false)
    private Stock stock;

    private LocalDateTime createdAt;

    public void setUser(User user){
        this.user = user;
    }

    private UserInterestStock(){}

    @Builder
    public UserInterestStock(User user, Stock stock, LocalDateTime createdAt){
        this.user = user;
        this.stock = stock;
        this.createdAt = createdAt;
    }
}
