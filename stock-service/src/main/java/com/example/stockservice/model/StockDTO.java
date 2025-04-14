package com.example.stockservice.model;

import com.example.stockservice.domain.DailySummaryStock;
import com.example.stockservice.domain.UserInterestStock;
import lombok.Data;

import java.util.List;

@Data
public class StockDTO {
    private String code;
    private String name;
    private String market;

    private List<DailySummaryStock> dailySummaryStocks;
    private List<UserInterestStock> userInterestStocks;
}
