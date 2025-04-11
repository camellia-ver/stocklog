package com.example.stockservice.domain.common;

import jakarta.persistence.Embeddable;
import lombok.Getter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Getter
@Embeddable
public class BaseTimeEntity{
    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    protected BaseTimeEntity(){}
}
