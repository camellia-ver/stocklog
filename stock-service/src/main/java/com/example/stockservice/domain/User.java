package com.example.stockservice.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

@Table(name = "user")
@Getter
@Entity
public class User implements UserDetails, Serializable {
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", updatable = false)
    private Long id;

    // 닉네임
    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "email", nullable = false, unique = true)
    private String email;

    @Column(name = "password", nullable = false)
    private String password;

    @ManyToMany
    @JoinTable(
            name = "user_favorite_stock",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "stock_id")
    )
    private List<Stock> favoriteStocks;

    @Column(name = "create_dt",nullable = false)
    private LocalDateTime createDate;

    private User(){}

    @Builder
    public User(String name,String email,String password,
                List<Stock> favoriteStocks,LocalDateTime createDate){
        this.name = name;
        this.email = email;
        this.password = password;
        this.favoriteStocks = (favoriteStocks != null) ? favoriteStocks : new ArrayList<>();
        this.createDate = (createDate != null) ? createDate : LocalDateTime.now();
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Arrays.asList(new SimpleGrantedAuthority("ROLE_USER"));
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
            return email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;  // 기본적으로 만료되지 않은 계정
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;  // 기본적으로 잠기지 않은 계정
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;  // 기본적으로 자격 증명이 만료되지 않음
    }

    @Override
    public boolean isEnabled() {
        return true;  // 기본적으로 활성화된 계정
    }
}
