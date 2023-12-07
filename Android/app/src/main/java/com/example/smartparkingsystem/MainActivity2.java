package com.example.smartparkingsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;

//This page is for parking reservations


public class MainActivity2 extends AppCompatActivity {
    TextView text2;
    Button button2;
    private TextView textViewSelectedDate;
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

        textViewSelectedDate = findViewById(R.id.textViewSelectedDate);

        // Set up a click listener for the text view
        textViewSelectedDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showDatePickerDialog();
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

    private void showDatePickerDialog() {
        // Get the current date
        Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int dayOfMonth = calendar.get(Calendar.DAY_OF_MONTH);

        // Create a DatePickerDialog with the current date as the default and a minimum date
        DatePickerDialog datePickerDialog = new DatePickerDialog(
                this,
                (view, selectedYear, selectedMonth, selectedDayOfMonth) -> {
                    // Handle the selected date
                    // You can update your UI or save the selected date here

                    // Display the selected date on the text view
                    displaySelectedDate(selectedYear, selectedMonth, selectedDayOfMonth);
                },
                year, month, dayOfMonth);

        // Set the minimum date to the current date
        datePickerDialog.getDatePicker().setMinDate(System.currentTimeMillis() - 1000);

        // Show the dialog
        datePickerDialog.show();
    }

    private void displaySelectedDate(int year, int month, int dayOfMonth) {
        // Format the selected date
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        Calendar selectedCalendar = Calendar.getInstance();
        selectedCalendar.set(year, month, dayOfMonth);
        String formattedDate = dateFormat.format(selectedCalendar.getTime());

        // Display the selected date on the text view
        textViewSelectedDate.setText(formattedDate);
    }



}