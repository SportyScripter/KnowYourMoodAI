package com.example.mobile_kymai;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class mood_recognition extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_mood_recognition);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        String mood = getIntent().getStringExtra("EXTRA_MOOD");
        TextView txtViewYourMood = findViewById(R.id.txtViewYourMood);
        txtViewYourMood.setText(mood != null ? mood : "Brak Danych");
    }
    public void btnReturn(View v) {
        Intent intent = new Intent(this, SelectMenu.class);
        startActivity(intent);

    }
    public void btnExit(View v) {
        Toast.makeText(this, "Aplikacja została zamknięta", Toast.LENGTH_SHORT).show();
        finishAffinity();
        System.exit(0);
    }
}