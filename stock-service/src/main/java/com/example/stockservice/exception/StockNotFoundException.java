package com.example.stockservice.exception;

public class StockNotFoundException extends RuntimeException{
    public StockNotFoundException(String code){
        super("해당 종목이 존재하지 않습니다: " + code);
    }
}
