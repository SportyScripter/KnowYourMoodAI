package com.example.mobile_kymai;

import java.util.List;

public class User {
    private String username;
    private String password;
    private String currentUser;
    private List<User> users;

    private User(String username,String password,String checkPassword){
        if (password.equals(checkPassword)){
            this.username = username;
            this.password = password;
        }
        else{
            throw new RuntimeException("Passwords are different");
        }

    }
}
