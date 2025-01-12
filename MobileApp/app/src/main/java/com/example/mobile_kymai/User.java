package com.example.mobile_kymai;

import java.util.List;

public class User {
    private String username;
    private String password;
    private String currentUser;
    private String email;
    private List<User> users;

    User(String username, String password, String email){
            this.username = username;
            this.password = password;
            this.email = email;
    }
}
