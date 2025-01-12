package com.example.mobile_kymai;

import android.content.ContentResolver;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.PickVisualMediaRequest;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONObject;

import java.io.InputStream;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class SelectMenu extends AppCompatActivity {
    private Uri myUri;
    private String mood;
    private static final Bundle CAMERA_PIC_REQUEST = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_select_menu);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);

            return insets;
        });
    }

    ActivityResultLauncher<PickVisualMediaRequest> pickMedia =
            registerForActivityResult(new ActivityResultContracts.PickVisualMedia(), uri -> {
                if (uri != null) {
                    myUri = uri;
                    Log.d("PhotoPicker", "Selected URI: " + myUri);
                    ImageView img = findViewById(R.id.imageView);
                    img.setImageURI(uri);
                } else {
                    Log.d("PhotoPicker", "No media selected");
                }
            });


    public void btnReturn(View v) {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);

    }

    public void btnOpenCamera(View v) {
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        startActivity(cameraIntent, CAMERA_PIC_REQUEST);
    }

    public void btnOpenGallery(View v) {
        pickMedia.launch(new PickVisualMediaRequest.Builder()
                .setMediaType(ActivityResultContracts.PickVisualMedia.ImageOnly.INSTANCE)
                .build());
    }

    public void btnSendImg(View view) {
        new Thread(() -> {
            try {
                // Przekształcenie Uri w plik lub InputStream
                ContentResolver contentResolver = getContentResolver();
                InputStream inputStream = contentResolver.openInputStream(myUri);

                // Konwersja InputStream na RequestBody
                byte[] buffer = new byte[inputStream.available()];
                inputStream.read(buffer);
                RequestBody fileBody = RequestBody.create(
                        buffer,
                        MediaType.parse("image/jpeg") // Typ MIME pliku
                );

                // Budowanie części multipart
                MultipartBody.Part filePart = MultipartBody.Part.createFormData(
                        "file",   // Klucz pola zgodny z FastAPI
                        "photo.jpg",  // Nazwa pliku
                        fileBody
                );

                // Konfiguracja klienta HTTP
                OkHttpClient client = new OkHttpClient();
                Request request = new Request.Builder()
                        .url(ApiConfig.BASE_URL+"/analyze-emotion/") // Zamień na odpowiedni adres URL
                        .post(new MultipartBody.Builder()
                                .setType(MultipartBody.FORM)
                                .addPart(filePart)
                                .build())
                        .build();

                // Wysłanie żądania i obsługa odpowiedzi
                Response response = client.newCall(request).execute();
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();
                    JSONObject jsonResponse = new JSONObject(responseBody);
                    Intent intent = new Intent(this, mood_recognition.class);
                    mood = jsonResponse.getString("emotion").toUpperCase();
                    runOnUiThread(() -> {
                        Toast.makeText(getApplicationContext(), "Odpowiedź: " + mood, Toast.LENGTH_LONG).show();
                        Log.d("SendImage","Odpowiedź: "+mood);
                    });
                    intent.putExtra("EXTRA_MOOD",mood);
                    startActivity(intent);
                } else {
                    runOnUiThread(() -> {
                        Toast.makeText(getApplicationContext(), "Błąd: " + response.code(), Toast.LENGTH_LONG).show();
                        Log.d("SendImage","Odpowiedź: "+response.code());
                    });
                }

            } catch (Exception e) {
                runOnUiThread(() -> {
                    Toast.makeText(getApplicationContext(), "Wystąpił błąd: " + e.getMessage(), Toast.LENGTH_LONG).show();
                    Log.d("SendImage","Odpowiedź: "+e.getMessage());
                });
            }
        }).start();
    }

}

