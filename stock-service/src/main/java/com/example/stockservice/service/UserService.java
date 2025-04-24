package com.example.stockservice.service;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.domain.User;
import com.example.stockservice.domain.UserInterestStock;
import com.example.stockservice.exception.DuplicateUserException;
import com.example.stockservice.exception.PasswordMismatchException;
import com.example.stockservice.exception.StockNotFoundException;
import com.example.stockservice.model.InterestStockDTO;
import com.example.stockservice.model.UserDTO;
import com.example.stockservice.repository.StockRepository;
import com.example.stockservice.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Clock;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final StockRepository stockRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;
    private final Clock clock;

    @Transactional
    public void join(@Valid UserDTO dto){
        validateDuplicateUser(dto.getEmail());

        if (!dto.getPassword().equals(dto.getConfirmPassword())){
            throw new DuplicateUserException("이미 존재하는 이메일 주소입니다.");
        }

        String encodedPassword = bCryptPasswordEncoder.encode(dto.getPassword());

        if (!dto.getPassword().equals(dto.getConfirmPassword())) {
            throw new PasswordMismatchException("비밀번호가 일치하지 않습니다.");
        }

        User newUser = dto.toEntity(bCryptPasswordEncoder, clock);

        List<Stock> stocks = dto.getInterestStockList().stream()
                        .map(stockDTO -> stockRepository.findByCode(stockDTO.getCode())
                                .orElseThrow(() -> new StockNotFoundException(stockDTO.getCode())))
                                .toList();

        newUser.addInterestStock(stocks);
        userRepository.save(newUser);
    }

    private void validateDuplicateUser(String email){
        if (userRepository.existsByEmail(email)){
            throw new IllegalStateException("이미 존재하는 이메일 주소입니다.");
        }
    }
}
