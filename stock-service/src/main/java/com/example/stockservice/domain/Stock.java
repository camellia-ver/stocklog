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
    private int clpr;

    @Column(name = "vs", nullable = false)
    private int vs;

    @Column(name = "fltRt", nullable = false)
    private double fltRt;

    @Column(name = "mkp", nullable = false)
    private int mkp;

    @Column(name = "int", nullable = false)
    private int hipr;

    @Column(name = "lopr", nullable = false)
    private int lopr;

    @Column(name = "trqu", nullable = false)
    private int trqu;

    @Column(name = "trPrc", nullable = false)
    private int trPrc;

    @Column(name = "lstgStCnt", nullable = false)
    private int lstgStCnt;

    @Column(name = "mrktTotAmt", nullable = false)
    private int mrktTotAmt;

    private Stock(){}

    @Builder
    public Stock(Long srtnCd,String isinCd,String itmsNm,int clpr,int vs,
                 double fltRt,int mkp,int hipr,int lopr,int trqu,int trPrc,
                 int lstgStCnt,int mrktTotAmt){
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
