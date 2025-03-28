package com.example.stockservice.controller;

import com.example.stockservice.domain.User;
import com.example.stockservice.dto.UserDTO;
import com.example.stockservice.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/login")
    public String loginPage(){
        return "login";
    }

    @GetMapping("/signup")
    public String signupPage(Model model){
        model.addAttribute("type","user");
        return "signup";
    }

    @GetMapping("/setting")
    public String settingPage(Model model){
        model.addAttribute("type","setting");
        return "signup";
    }

    @PostMapping("/user")
    public String signup(@ModelAttribute UserDTO request, Model model){
        try{
            userService.join(request);
        }catch (Exception e){
            model.addAttribute("errorMessage", e.getMessage());
            return "signup";
        }

        return "redirect:/login";
    }

    @GetMapping("/logout")
    public String logout(HttpServletRequest request, HttpServletResponse response){
        new SecurityContextLogoutHandler().logout(request, response,
                SecurityContextHolder.getContext().getAuthentication());

        return "redirect:/login";
    }
}
