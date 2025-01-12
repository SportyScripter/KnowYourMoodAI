package com.example.mobile_kymai;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.IOException;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Register extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_register);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void BtnRegister(View v) {
        EditText EdtPassword = findViewById(R.id.edtTxtPassword);
        EditText EdtRepeatPassword = findViewById(R.id.edtTxtRepeatPassword);
        EditText EdtUsername = findViewById(R.id.edtTxtUsername);
        EditText UserEmail = findViewById(R.id.edtTxtEmail);
        String email = UserEmail.getText().toString();
        String username = EdtUsername.getText().toString();
        String password = EdtPassword.getText().toString();
        String repeatPassword = EdtRepeatPassword.getText().toString();
        if (password.equals(repeatPassword)) {
            Toast.makeText(this, "Pomyślnie zarejestrowano", Toast.LENGTH_SHORT).show();
            OkHttpClient client = new OkHttpClient();
            RequestBody formBody = new FormBody.Builder().add("username", username).add("email", email).add("password", password).build();
            Request request = new Request.Builder().url("http://192.168.1.111:8000/register/").post(formBody).build();
            new Thread(()->{
                try {
                    Response response = client.newCall(request).execute();
                    if (response.isSuccessful()){
                        String responseBody = response.body().toString();
                        runOnUiThread(()->{
                            Toast.makeText(getApplicationContext(), "Rejestracja udana!", Toast.LENGTH_SHORT).show();
                            Intent intent = new Intent(this, Login.class);
                            startActivity(intent);
                        });

                    }else{
                        String errorBody = response.body().toString();
                        runOnUiThread(()->{
                            Toast.makeText(getApplicationContext(), "Błąd rejestracji: " + errorBody, Toast.LENGTH_SHORT).show();
                        });
                    }
                } catch (Exception e) {
                    runOnUiThread(()->{
                        Toast.makeText(getApplicationContext(), "Wystąpił błąd: "+e.getMessage(), Toast.LENGTH_SHORT).show();
                    });
                }
            }).start();
        } else {
            Toast.makeText(this, "Dane są nieprawidłowe", Toast.LENGTH_SHORT).show();
        }
    }

    public void BtnReturn(View v) {
        Intent intent = new Intent(this, Login.class);
        startActivity(intent);
    }

    public void btnExit(View v) {
        Toast.makeText(this, "Aplikacja została zamknięta", Toast.LENGTH_SHORT).show();
        finishAffinity();
        System.exit(0);
    }
}