package com.example.stockservice.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;

@Configuration
public class config {
    @Bean
    public Clock clock(){
        return Clock.systemUTC();
    }
}
