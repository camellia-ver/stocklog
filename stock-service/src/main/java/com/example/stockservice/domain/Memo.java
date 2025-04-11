package com.example.stockservice.domain;

import com.example.stockservice.domain.common.BaseTimeEntity;
import com.example.stockservice.domain.common.BaseIdEntity;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

@Entity
@Table(name = "memo")
@Getter
public class Memo extends BaseIdEntity {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "stock_code", referencedColumnName = "code", nullable = false)
    private Stock stock;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String content;

    @Embedded
    private BaseTimeEntity timeInfo;

    @Builder
    public Memo(User user, Stock stock, String content){
        this.user = user;
        this.stock = stock;
        this.content = content;
    }
}
