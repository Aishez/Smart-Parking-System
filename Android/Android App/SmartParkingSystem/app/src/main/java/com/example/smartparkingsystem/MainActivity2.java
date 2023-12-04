package com.example.smartparkingsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

//This page is for parking reservations


public class MainActivity2 extends AppCompatActivity {
    TextView text2;
    Button button2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

//        text2=findViewById(R.id.text_hello);
//        Intent intent=getIntent();
//        String x= intent.getStringExtra(MainActivity.extra_text1);
//        text2.setText("The imported text is "+ x);
        button2=findViewById(R.id.button);
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent3= new Intent(MainActivity2.this, ConfirmActivity.class);

                //String sample_text=text.getText().toString();
                //intent1.putExtra(extra_text1, sample_text);
                startActivity(intent3);
            }
        });

        Spinner spinnerDaysOfWeek = findViewById(R.id.spinnerDaysOfWeek);

        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.days_of_week_array, android.R.layout.simple_spinner_item);

        // Specify the layout to use when the list of choices appears
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

        // Apply the adapter to the spinner
        spinnerDaysOfWeek.setAdapter(adapter);


    }



}