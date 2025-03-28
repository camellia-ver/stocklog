package com.example.stockservice.service;

import com.example.stockservice.domain.Stock;
import com.example.stockservice.domain.User;
import com.example.stockservice.dto.UserDTO;
import com.example.stockservice.repository.StockRepository;
import com.example.stockservice.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final StockRepository stockRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    @Transactional
    public void join(UserDTO dto){
        validateDuplicateUser(dto.getEmail());

        userRepository.save(User.builder()
                .name(dto.getName())
                .email(dto.getEmail())
                .password(bCryptPasswordEncoder.encode(dto.getPassword()))
                .favoriteStocks(reshapeToStockList(dto.getFavoriteStockList()))
                .createDate(LocalDateTime.now(ZoneOffset.UTC))
                .build());
    }

    private List<Stock> reshapeToStockList(List<String> favoriteStockList){
        List<Stock> result = new ArrayList<Stock>();

        if (!favoriteStockList.isEmpty()) {
            for (String stock : favoriteStockList) {
                Optional<Stock> stockOptional = stockRepository.findByIsinCd(stock);
                stockOptional.ifPresent(result::add);
            }
        }

        return result;
    }

    private void validateDuplicateUser(String mail){
        Optional<User> findUser = userRepository.findByEmail(mail);
        if (findUser.isPresent()){
            throw new IllegalStateException("이미 존재하는 이메일 주소입니다.");
        }
    }
}
