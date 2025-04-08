package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;

@Table(name = "user")
@Entity
public class UserInterestStock {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id", updatable = false)
    private Long id;

    @Column(name = "code", unique = true)
    private String code;
    @Column(name = "name")
    private String name;
    @Column(name = "market")
    private String market;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    private UserInterestStock(){}

    public void setUser(User user){
        this.user = user;
    }

    @Builder
    public UserInterestStock(String code, String name, String market){
        this.code = code;
        this.name = name;
        this.market = market;
    }
}
