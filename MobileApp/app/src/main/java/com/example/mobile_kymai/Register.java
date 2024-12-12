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
        String password = EdtPassword.getText().toString();
        String repeatPassword = EdtRepeatPassword.getText().toString();
        if (password.equals(repeatPassword)) {
            Toast.makeText(this, "Pomyślnie zarejestrowano", Toast.LENGTH_SHORT).show();
            Intent intent = new Intent(this, Login.class);
            startActivity(intent);
        } else {
            Toast.makeText(this, "Dane są nieprawidłowe", Toast.LENGTH_SHORT).show();
        }
    }

    public void BtnReturn(View v) {
        Intent intent = new Intent(this, Login.class);
        startActivity(intent);
    }

    public void BtnExit(View v) {
        Toast.makeText(this, "Aplikacja została zamknięta", Toast.LENGTH_SHORT).show();
        finishAffinity();
        System.exit(0);
    }
}