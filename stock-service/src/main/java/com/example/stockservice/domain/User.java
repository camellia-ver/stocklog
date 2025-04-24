package com.example.stockservice.domain;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import org.hibernate.annotations.CreationTimestamp;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.io.Serial;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Entity
@Table(name = "user")
@Getter
public class User implements UserDetails, Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 닉네임
    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "email", nullable = false, unique = true)
    private String email;

    @JsonIgnore
    @Column(name = "password", nullable = false)
    private String password;

    @CreationTimestamp
    @Column(name = "create_dt", nullable = false)
    private LocalDateTime createDate;

    @JsonIgnore
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Memo> memos = new ArrayList<>();

    @JsonIgnore
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<UserInterestStock> interestStocks = new ArrayList<>();

    public void addInterestStock(Stock stock){
        UserInterestStock userInterestStock = UserInterestStock.builder()
                .user(this)
                .stock(stock)
                .createdAt(LocalDateTime.now())
                .build();
        this.interestStocks.add(userInterestStock);
    }

    public void addInterestStock(List<Stock> stocks){
        for (Stock stock : stocks){
            this.addInterestStock(stock);
        }
    }

    private User(){}

    @Builder
    public User(String name, String email, String password,
                List<UserInterestStock> interestStocks , LocalDateTime createDate){
        this.name = name;
        this.email = email;
        this.password = password;
        this.interestStocks = interestStocks;
        this.createDate = (createDate != null) ? createDate : LocalDateTime.now();
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_USER"));
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
