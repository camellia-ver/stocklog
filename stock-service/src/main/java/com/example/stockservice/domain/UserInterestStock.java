package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

@Entity
@Getter
public class UserInterestStock {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "code", nullable = false)
    private String code;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "market", nullable = false)
    private String market;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    public void setUser(User user){
        this.user = user;
    }

    private UserInterestStock(){}

    @Builder
    public UserInterestStock(String code, String name, String market){
        this.code = code;
        this.name = name;
        this.market = market;
    }
}
