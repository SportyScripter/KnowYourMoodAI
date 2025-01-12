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

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Login extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_login);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void OnClickLogin(View v) {
        EditText edtTxtUsername = findViewById(R.id.edtTxtUsername);
        EditText edtTxtPassword = findViewById(R.id.edtTxtPassword);
        String username = edtTxtUsername.getText().toString();
        String password = edtTxtPassword.getText().toString();
        new Thread(() -> {
            try {
                OkHttpClient client = new OkHttpClient();
                RequestBody formBody = new FormBody.Builder()
                        .add("username", username)
                        .add("password", password)
                        .build();
                Request request = new Request.Builder().url(ApiConfig.BASE_URL + "/login/").post(formBody).build();
                Response response = client.newCall(request).execute();
                if (response.isSuccessful()) {
                    String responseBody = response.body().toString();
                    runOnUiThread(() -> {
                        Toast.makeText(getApplicationContext(), "Logowanie udane!", Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(this, MainActivity.class);
                        startActivity(intent);
                    });
                } else {
                    String errorBody = response.body().toString();
                    runOnUiThread(() -> {
                        Toast.makeText(getApplicationContext(), "Logowanie niepowiodło się: " + errorBody, Toast.LENGTH_SHORT).show();
                    });
                }
            } catch (Exception e) {
                runOnUiThread(() -> {
                    Toast.makeText(getApplicationContext(), "Wystąpił błąd: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }

    public void OnClickRegister(View V) {
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
    }

    public void btnExit(View v) {
        Toast.makeText(this, "Aplikacja została zamknięta", Toast.LENGTH_SHORT).show();
        finishAffinity();
        System.exit(0);
    }
}