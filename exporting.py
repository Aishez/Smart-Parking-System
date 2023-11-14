import numpy as np
import time
import cv2
from datetime import datetime
import csv



ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}



def merge_time_periods(time_list):
    if not time_list:
        return []

    merged = [time_list[0]]
    for current in time_list[1:]:
        last = merged[-1]
        if last[1] == current[0]:
            merged[-1] = (last[0], current[1])  # merge with last period
        else:
            merged.append(current)  # start a new period

    return merged



def export_to_csv(slot_data, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Slot ID', 'Currently Occupied', 'Slot Counter'])

        for slot_id, data in enumerate(slot_data, start=1):
            writer.writerow([slot_id, data['currently_occupied'], data['slot_counter']])



def aruco_display(corners, ids, image, slot_timers, slot_occupancy, slot_records, final_time_list, slot_counters, hourly_slot_sets):
    if len(corners) > 0:
        slots = [0] * 5  # Initialize slots for different X-coordinate ranges
        current_time = datetime.now()

        for slot_index in range(5):
            if slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                # Slot was occupied for more than 5 seconds, record exit time and update status
                exit_time = current_time
                slot_records[slot_index].append(
                    (slot_timers[slot_index], exit_time))
                final_time_list[slot_index].append(
                    # Update final time list
                    (slot_timers[slot_index], exit_time))

                # Extract hourly intervals from merged_time_list for the current slot
                merged_time_list = final_time_list[slot_index]
                for entry, exit_time in merged_time_list:
                    start_hour = entry.hour
                    end_hour = exit_time.hour

                    if entry.minute > 0 or entry.second > 0:
                        start_hour += 1

                    if exit_time.minute > 0 or exit_time.second > 0:
                        end_hour += 1

                    # If start and end hour are the same, add the hour as a single element
                    if start_hour == end_hour:
                        hourly_slot_sets[slot_index].append([start_hour])
                    else:
                        # Add all hours in between
                        hours_in_interval = list(range(start_hour, end_hour))
                        # Exclude the last hour if the minute is 00 for the end hour
                        if exit_time.minute == 0:
                            hours_in_interval = hours_in_interval[:-1]

                        hourly_slot_sets[slot_index].append(hours_in_interval)

                # Recalculate the activated slots for the last interval in the merged list
                last_entry, last_exit = merged_time_list[-1]
                start_hour = last_entry.hour
                end_hour = last_exit.hour
                if last_entry.minute > 0 or last_entry.second > 0:
                    start_hour += 1
                if last_exit.minute > 0 or last_exit.second > 0:
                    end_hour += 1
                hourly_slot_sets[slot_index] = [list(range(start_hour, end_hour + 1))]

                slot_occupancy[slot_index] = "Not Occupied"
                slot_timers[slot_index] = None

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # Convert coordinates to integers
            topLeft = tuple(map(int, topLeft))
            topRight = tuple(map(int, topRight))
            bottomRight = tuple(map(int, bottomRight))
            bottomLeft = tuple(map(int, bottomLeft))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(image, str(markerID), topLeft, cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

            # Update slots based on marker IDs
            slot_index = markerID[0] - 1  # Slot index is 0-based

            if 0 <= slot_index < 5:
                if slot_timers[slot_index] is None and slot_occupancy[slot_index] == "Not Occupied":
                    # Slot was unoccupied and is now occupied, record entry time
                    slot_timers[slot_index] = current_time
                    slot_occupancy[slot_index] = "Occupied"
                    slot_counters[slot_index] += 1  # Increment the counter
                elif slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                    # Slot was occupied for more than 5 seconds, record exit time and update status
                    exit_time = current_time
                    slot_records[slot_index].append((slot_timers[slot_index], exit_time))
                    final_time_list[slot_index].append(
                        (slot_timers[slot_index], exit_time))  # Update final time list

                    # Calculate the hourly slots during which the slot was occupied
                    start_hour = slot_timers[slot_index].hour
                    end_hour = exit_time.hour
                    if slot_timers[slot_index].minute > 0 or slot_timers[slot_index].second > 0:
                        start_hour += 1
                    if exit_time.minute > 0 or exit_time.second > 0:
                        end_hour += 1
                    hourly_slots = set(range(start_hour, end_hour))
                    hourly_slot_sets[slot_index].update(hourly_slots)

                    slot_occupancy[slot_index] = "Not Occupied"
                    slot_timers[slot_index] = None

        return image, slots, slot_occupancy, final_time_list, hourly_slot_sets
    else:
        current_time = datetime.now()
        for slot_index in range(5):
            if slot_timers[slot_index] is not None and (current_time - slot_timers[slot_index]).total_seconds() >= 5:
                # Slot was occupied for more than 5 seconds, record exit time and update status
                exit_time = current_time
                slot_records[slot_index].append(
                    (slot_timers[slot_index], exit_time))
                final_time_list[slot_index].append(
                    # Update final time list
                    (slot_timers[slot_index], exit_time))

                # Extract hourly intervals from merged_time_list for the current slot
                merged_time_list = final_time_list[slot_index]
                for entry, exit_time in merged_time_list:
                    start_hour = entry.hour
                    end_hour = exit_time.hour

                    if entry.minute > 0 or entry.second > 0:
                        start_hour += 1

                    if exit_time.minute > 0 or exit_time.second > 0:
                        end_hour += 1

                    # If start and end hour are the same, add the hour as a single element
                    if start_hour == end_hour:
                        hourly_slot_sets[slot_index].append([start_hour])
                    else:
                        # Add all hours in between
                        hours_in_interval = list(range(start_hour, end_hour))
                        # Exclude the last hour if the minute is 00 for the end hour
                        if exit_time.minute == 0:
                            hours_in_interval = hours_in_interval[:-1]

                        hourly_slot_sets[slot_index].append(hours_in_interval)

                # Recalculate the activated slots for the last interval in the merged list
                last_entry, last_exit = merged_time_list[-1]
                start_hour = last_entry.hour
                end_hour = last_exit.hour
                if last_entry.minute > 0 or last_entry.second > 0:
                    start_hour += 1
                if last_exit.minute > 0 or last_exit.second > 0:
                    end_hour += 1
                hourly_slot_sets[slot_index] = [list(range(start_hour, end_hour + 1))]

                slot_occupancy[slot_index] = "Not Occupied"
                slot_timers[slot_index] = None

        return image, None, None, final_time_list, hourly_slot_sets



aruco_type = "DICT_4X4_250"
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])
arucoParams = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

slot_timers = [None] * 5
slot_occupancy = ["Not Occupied"] * 5
slot_records = [[] for _ in range(5)]
final_time_list = [[] for _ in range(5)]
slots = [0] * 5
slot_counters = [0] * 5
hourly_slot_sets = [[] for _ in range(5)]

start_time = time.time()
slot_reset_interval = 5
print_interval = 10
last_print_time = start_time

while cap.isOpened():
    ret, img = cap.read()
    h, w, _ = img.shape
    width = 1000
    height = int(width * (h / w))
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    corners, ids, _ = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)

    if len(corners) > 0:
        detected_markers, updated_slots, updated_occupancy, final_time_list, hourly_slot_sets = aruco_display(
            corners, ids, img, slot_timers, slot_occupancy, slot_records, final_time_list, slot_counters, hourly_slot_sets)
        if updated_slots is not None:
            slots = updated_slots
            slot_occupancy = updated_occupancy
        cv2.imshow("Image", detected_markers)
    else:
        cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    current_time = time.time()

    if current_time - last_print_time >= print_interval:
        last_print_time = current_time
        print("Slot contents after {} seconds:".format(print_interval))

        slot_data_for_export = []
        for i in range(5):
            merged_time_list = merge_time_periods([(entry.strftime('%Y-%m-%d %H:%M:%S'), exit.strftime('%Y-%m-%d %H:%M:%S')) for entry, exit in final_time_list[i]])
            slot_counters[i] = len(merged_time_list)

            # Append slot data for export
            slot_data_for_export.append({
                'currently_occupied': slot_occupancy[i],
                'slot_counter': slot_counters[i]
            })

            print(f"Slot {i + 1} Counter:", slot_counters[i])
            print(f"Slot {i + 1} Occupancy:", slot_occupancy[i])
            print(f"Slot {i + 1} Hourly Set:", hourly_slot_sets[i])
            print("Final Time List for Slot {}: {}".format(i + 1, merged_time_list))

        # Export slot data to CSV
        export_to_csv(slot_data_for_export, 'slot_data.csv')

        print("\n")

cv2.destroyAllWindows()
cap.release()