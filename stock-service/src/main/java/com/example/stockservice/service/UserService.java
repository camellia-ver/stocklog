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

        String encodedPassword = Optional.ofNullable(dto.getPassword())
                        .map(bCryptPasswordEncoder::encode)
                                .orElseThrow(() -> new IllegalArgumentException("비밀번호는 필수 입력값입니다."));

        List<Stock> favoriteStocks = reshapeToStockList(dto.getFavoriteStockList());

        User newUser = User.builder()
                .name(dto.getName())
                .email(dto.getEmail())
                .password(encodedPassword)
                .favoriteStocks(favoriteStocks)
                .createDate(LocalDateTime.now(ZoneOffset.UTC))
                .build();

        userRepository.save(newUser);
    }

    private List<Stock> reshapeToStockList(List<String> favoriteStockList){
        List<Stock> result = new ArrayList<Stock>();

        if (!favoriteStockList.isEmpty()) {
            for (String stock : favoriteStockList) {
                Stock stockEntity = stockRepository.findByIsinCd(stock)
                        .orElseThrow(() -> new IllegalArgumentException("존재하지 않는 종목 코드입니다: " + stock));
                result.add(stockEntity);
            }
        }

        return result;
    }

    private void validateDuplicateUser(String email){
        if (userRepository.existByEmail(email)){
            throw new IllegalStateException("이미 존재하는 이메일 주소입니다.");
        }
    }


}
