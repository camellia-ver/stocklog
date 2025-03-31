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
    private String srtnCd;

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
    private Long trqu;

    @Column(name = "trPrc", nullable = false)
    private Long trPrc;

    @Column(name = "lstgStCnt", nullable = false)
    private Long lstgStCnt;

    @Column(name = "mrktTotAmt", nullable = false)
    private Double mrktTotAmt;

    private Stock(){}

    @Builder
    public Stock(String srtnCd,String isinCd,String itmsNm,String mrktCtg,
                 Integer clpr,Integer vs, Double fltRt,Integer mkp,Integer hipr,
                 Integer lopr,Long trqu, Long trPrc, Long lstgStCnt,
                 Double mrktTotAmt){
        this.srtnCd = srtnCd;
        this.isinCd = isinCd;
        this.itmsNm = itmsNm;
        this.mrktCtg = mrktCtg;
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
