package com.example.stockservice.service;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.domain.User;
import com.example.stockservice.dto.UserDTO;
import com.example.stockservice.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    @Transactional
    public void join(UserDTO dto){

        userRepository.save(User.builder()
                .name(dto.getName())
                .email(dto.getEmail())
                .password(bCryptPasswordEncoder.encode(dto.getPassword()))
                .favoriteStocks(reshapeToStockList(dto.getFavoriteStockList()))
                .createDate(LocalDateTime.now(ZoneOffset.UTC))
                .build());
    }

    private List<Stock> reshapeToStockList(List<String> favoriteStockList){
        List<Stock> test = null;
        return test;
    }

    private void validateDuplicateUser(String mail){

    }
}
