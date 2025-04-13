package com.example.stockservice.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class StockController {
    @GetMapping("/dashboard")
    public String signupPage(){
        return "dashboard";
    }
}
