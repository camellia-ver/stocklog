package com.example.stockservice.model;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.domain.User;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class InterestStockDTO {
    private String code;
}
