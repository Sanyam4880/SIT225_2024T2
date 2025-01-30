import serial
import time
import random

# Initialize serial communication with Arduino
arduino = serial.Serial('COM8', 9600, timeout=2)
time.sleep(2)  # Allow Arduino to initialize

# Main loop
while True:
    blink_count = random.randint(1, 5)  # Generate random blink count
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Sending blink count: {blink_count}")
    arduino.write(f'{blink_count}\n'.encode())  # Send blink count to Arduino

    time.sleep(0.5)  # Allow Arduino time to process

    # Variables to track Arduino responses
    received_blink_completed = False  
    wait_time = 1  # Default wait time
    start_time = time.time()  # Timeout mechanism

    while True:
        # Check for timeout to avoid infinite loop
        if time.time() - start_time > 10:  # Timeout after 10 seconds
            print(f"[{timestamp}] __________.")
            break

        if arduino.in_waiting > 0:  # Check if there's data to read
            arduino_response = arduino.readline().decode().strip()
            print(f"[{timestamp}] Received from Arduino: {arduino_response}")

            # Check for specific responses
            if "Blink completed" in arduino_response:
                received_blink_completed = True
            if "Received blink duration" in arduino_response:
                try:
                    wait_time = int(arduino_response.split(": ")[1])
                except (IndexError, ValueError):
                    print(f"[{timestamp}] Error parsing blink duration. Response: {arduino_response}")

        # Exit loop if blink is completed and wait_time is set
        if received_blink_completed and wait_time > 0:
            break

    # Print waiting message and delay before next iteration
    print(f"[{timestamp}] Waiting for {wait_time} seconds...\n")
    time.sleep(wait_time)