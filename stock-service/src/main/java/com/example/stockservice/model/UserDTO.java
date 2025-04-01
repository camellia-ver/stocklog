package com.example.stockservice.model;

import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;
import java.util.List;

@Data
public class UserDTO {
    private String name;
    private String email;

    @Size(min = 8, message = "비밀번호는 최소 8자 이상이여야 합니다.")
    @Pattern(regexp = "^(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]+$",
        message = "비밀번호는 영문, 숫자, 특수문자를 포함해야 합니다.")
    private String password;
    private String confirmPassword;

    private List<String> favoriteStockList;
}
