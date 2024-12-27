// Define an array to hold the LED pin numbers
int ledPins[] = {2, 3, 4, 5, 6};  

void setup() {

  Serial.begin(9600);

  // Initialize each LED pin as an output
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);  
  }
}

void loop() {
  // Check if at least 5 bytes are available from the serial input
  if (Serial.available() >= 5) {  
   
    for (int i = 0; i < 5; i++) {
      // Read the serial data for the current finger state (either 0 or 1)
      int fingerState = Serial.read();  

      
      digitalWrite(ledPins[i], fingerState == 1 ? HIGH : LOW);  
    }
  }
}
