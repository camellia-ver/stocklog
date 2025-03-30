package com.example.stockservice.model;

import lombok.Data;
import java.util.List;

@Data
public class UserDTO {
    private String name;
    private String email;
    private String password;
    private List<String> favoriteStockList;
}
