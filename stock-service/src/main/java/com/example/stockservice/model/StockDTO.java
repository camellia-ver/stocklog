package com.example.stockservice.model;

import lombok.*;

@Data
public class StockDTO {
    private String srtnCd;
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
    private Double mrktTotAmt;
}
