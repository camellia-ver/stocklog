package com.example.stockservice.domain;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "stock")
@Getter
public class Stock {
    @Id
    @Column(name = "code", length = 20)
    private String code;

    private String name;
    private String market;

    @OneToMany(mappedBy = "stock", cascade = CascadeType.ALL)
    @JsonManagedReference
    private List<Memo> memos = new ArrayList<>();

    @OneToMany(mappedBy = "stock", cascade = CascadeType.ALL)
    private List<DailySummaryStock> dailySummaryStocks;

    @OneToMany(mappedBy = "stock", cascade = CascadeType.ALL)
    private List<UserInterestStock> userInterestStocks;
}
