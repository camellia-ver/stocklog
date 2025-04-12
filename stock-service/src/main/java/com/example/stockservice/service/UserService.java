package com.example.stockservice.service;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.domain.User;
import com.example.stockservice.domain.UserInterestStock;
import com.example.stockservice.model.InterestStockDTO;
import com.example.stockservice.model.UserDTO;
import com.example.stockservice.repository.StockRepository;
import com.example.stockservice.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

    @Transactional
    public void join(@Valid UserDTO dto){
        validateDuplicateUser(dto.getEmail());

        if (!dto.getPassword().equals(dto.getConfirmPassword())){
            throw new IllegalStateException("비밀번호가 일치하지 않습니다.");
        }

        String encodedPassword = Optional.of(dto.getPassword())
                        .map(bCryptPasswordEncoder::encode)
                                .orElseThrow(() -> new IllegalArgumentException("비밀번호는 필수 입력값입니다."));

        User newUser = User.builder()
                .name(dto.getName())
                .email(dto.getEmail())
                .interestStocks(new ArrayList<>())
                .password(encodedPassword)
                .createDate(LocalDateTime.now(ZoneOffset.UTC))
                .build();

        for (InterestStockDTO stockDTO : dto.getInterestStockList()){
            Stock stock = stockRepository.findByCode(stockDTO.getCode())
                    .orElseThrow(() -> new IllegalArgumentException("해당 종목이 존재하지 않습니다: " + stockDTO.getCode()));

            newUser.addInterestStock(stock);
        }

        userRepository.save(newUser);
    }

    private void validateDuplicateUser(String email){
        if (userRepository.existsByEmail(email)){
            throw new IllegalStateException("이미 존재하는 이메일 주소입니다.");
        }
    }
}
