const int ledPin = 13;  // LED connected to pin 13
int blinkCount = 1;  // Default number of blinks

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String inputString = Serial.readStringUntil('\n'); // Read input
        blinkCount = inputString.toInt();  // Convert to integer

        // Send acknowledgment to Python
        Serial.print("Received blink count: ");
        Serial.println(blinkCount);

        // Blink LED
        for (int i = 0; i < blinkCount; i++) {
            digitalWrite(ledPin, HIGH);
            delay(500);  // LED ON for 500ms
            digitalWrite(ledPin, LOW);
            delay(500);  // LED OFF for 500ms
        }

        // Generate random wait time (between 1 to 5 seconds)
        int waitTime = random(1, 6);
        Serial.print("Wait time: ");
        Serial.println(waitTime);

        delay(waitTime * 1000);  // Delay before accepting new command
    }
}