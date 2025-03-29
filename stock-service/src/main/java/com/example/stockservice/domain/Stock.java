package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Table(name = "stock")
@Getter
@Entity
public class Stock {
    @Id
    @Column(name = "srtnCd", updatable = false)
    private Long srtnCd;

    @ManyToMany(mappedBy = "favoriteStocks")
    private List<User> users;

    @Column(name = "isinCd", nullable = false)
    private String isinCd;

    @Column(name = "itmsNm", nullable = false)
    private String itmsNm;

    @Column(name = "mrktCtg", nullable = false)
    private String mrktCtg;

    @Column(name = "clpr", nullable = false)
    private Integer clpr;

    @Column(name = "vs", nullable = false)
    private Integer vs;

    @Column(name = "fltRt", nullable = false)
    private Double fltRt;

    @Column(name = "mkp", nullable = false)
    private Integer mkp;

    @Column(name = "hipr", nullable = false)
    private Integer hipr;

    @Column(name = "lopr", nullable = false)
    private Integer lopr;

    @Column(name = "trqu", nullable = false)
    private Integer trqu;

    @Column(name = "trPrc", nullable = false)
    private Integer trPrc;

    @Column(name = "lstgStCnt", nullable = false)
    private Integer lstgStCnt;

    @Column(name = "mrktTotAmt", nullable = false)
    private Integer mrktTotAmt;

    private Stock(){}

    @Builder
    public Stock(Long srtnCd,String isinCd,String itmsNm,Integer clpr,Integer vs,
                 Double fltRt,Integer mkp,Integer hipr,Integer lopr,Integer trqu,
                 Integer trPrc, Integer lstgStCnt,Integer mrktTotAmt){
        this.srtnCd = srtnCd;
        this.isinCd = isinCd;
        this.itmsNm = itmsNm;
        this.clpr = clpr;
        this.vs = vs;
        this.fltRt = fltRt;
        this.mkp = mkp;
        this.hipr = hipr;
        this.lopr = lopr;
        this.trqu = trqu;
        this.trPrc = trPrc;
        this.lstgStCnt = lstgStCnt;
        this.mrktTotAmt = mrktTotAmt;
    }
}
