package com.example.stockservice.dto;

import com.example.stockservice.domain.User;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class StockDTO {
    private Long srtnCd;
    private List<User> users;
    private String isinCd;
    private String itmsNm;
    private String mrktCtg;
    private Integer clpr;
    private Integer vs;
    private Double fltRt;
    private Integer mkp;
    private Integer hipr;
    private Integer lopr;
    private Integer trqu;
    private Integer trPrc;
    private Integer lstgStCnt;
    private Integer mrktTotAmt;
}
