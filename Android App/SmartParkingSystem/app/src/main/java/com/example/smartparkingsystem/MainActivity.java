package com.example.smartparkingsystem;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

//import com.google.firebase.FirebaseApp;

public class MainActivity extends AppCompatActivity {
    TextView text;
    Button button;
    public static final String extra_text1="com.example.smartparkingsystem.extra.text1";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //FirebaseApp.initializeApp(this);

        text=findViewById(R.id.text_sample);
        //text.setText("This is a Sample Text");



        button=findViewById(R.id.button1);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent1= new Intent(MainActivity.this, Parking_spaces_activity.class);

                String sample_text=text.getText().toString();
                intent1.putExtra(extra_text1, sample_text);
                startActivity(intent1);
            }
        });
    }

//    public void OpenActivity(View v){
//        Intent intent1= new Intent(this,MainActivity2.class);
//        text=findViewById(R.id.text_sample);
//        text.setText("This is a Sample Text");
//        String sample_text=text.getText().toString();
//        intent1.putExtra(extra_text1, sample_text);
//        startActivity(intent1);
//    }

}