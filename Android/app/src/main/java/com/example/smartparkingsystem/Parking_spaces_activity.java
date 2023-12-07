package com.example.smartparkingsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Parking_spaces_activity extends AppCompatActivity {

    private static final int TOTAL_SLOTS = 20;
    private static final int OCCUPIED_SLOTS = 5;
    //    private ArrayAdapter<Boolean> adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_parking_spaces);

        GridLayout gridLayout = findViewById(R.id.gridLayout);

        // Create parking slots availability list
        List<Boolean> slotAvailability = new ArrayList<>();
        for (int i = 0; i < TOTAL_SLOTS; i++) {
            slotAvailability.add(i >= OCCUPIED_SLOTS); // Set to true for available slots
        }

        Collections.shuffle(slotAvailability);

        int numRows = 10; // Total rows
        int numCols = 3; // Total columns

        for (int row = 0; row < numRows; row++) {
            for (int col = 0; col < numCols; col++) {
                int slotIndex = row * numCols + col;

                if (col == 1) {
                    // Empty column with a downwards arrow
                    Button emptySlotButton = new Button(this);
                    GridLayout.LayoutParams layoutParams=new GridLayout.LayoutParams();
                    layoutParams.width=500;
                    layoutParams.height=150;
                    emptySlotButton.setBackgroundColor(Color.TRANSPARENT);
                    emptySlotButton.setLayoutParams(layoutParams);
//                    emptySlotButton.setVisibility(View.INVISIBLE); // Hide the empty slot
                    emptySlotButton.setText("↓");
                    emptySlotButton.setTextColor(Color.WHITE);
                    emptySlotButton.setTextSize(30);
                    gridLayout.addView(emptySlotButton);
                } else {
                    // Parking slots columns (1st and 3rd)
                    Button slotButton = new Button(this);
                    slotButton.setLayoutParams(new GridLayout.LayoutParams());
                    int a=(slotIndex+1)/3;
                    if ((slotIndex+1)%3==0){
                        slotButton.setText(String.valueOf(slotIndex + 1-a));}
                    else if ((slotIndex+1)%3!=0 && (slotIndex+1)>1){
                        slotButton.setText(String.valueOf(slotIndex + 1-((slotIndex)/3)));}
                    else{
                        slotButton.setText(String.valueOf(slotIndex + 1));
                    }
                    slotButton.setTextSize(18);
                    slotButton.setTextColor(Color.WHITE);

                    if (slotIndex >= 0 && slotIndex < slotAvailability.size() && slotAvailability.get(slotIndex)) {
                        slotButton.setBackgroundColor(Color.GREEN);
                        slotButton.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                bookParkingSlot((Button) view);
                            }
                        });
                    } else {
                        slotButton.setBackgroundColor(Color.RED);
                        slotButton.setEnabled(false);
                    }

                    gridLayout.addView(slotButton);
                }
            }
        }
    }

    private void bookParkingSlot(Button slotButton) {
        // Handle booking logic here
        String slotNumber = slotButton.getText().toString();
        Toast.makeText(this, "Booking Slot " + slotNumber, Toast.LENGTH_SHORT).show();
        Intent intent2= new Intent(Parking_spaces_activity.this, MainActivity2.class);
        startActivity(intent2);
        // Update slot availability and button appearance
//        slotButton.setBackgroundColor(Color.RED);
//        slotButton.setEnabled(false);
    }



}