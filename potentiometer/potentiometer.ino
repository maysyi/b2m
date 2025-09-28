int potPin = A0; // Potentiometer output connected to analog pin 3
int potVal = 0; // Variable to store the input from the potentiometer
int majPin = 2;
int minPin = 3;
int dimPin = 4;
int dom7Pin = 5;
int dim7Pin = 6;
int buttonState = 0;

void setup() {
  Serial.begin(115200);
  pinMode(majPin, INPUT_PULLUP);
  pinMode(minPin, INPUT_PULLUP);
  pinMode(dimPin, INPUT_PULLUP);
  pinMode(dom7Pin, INPUT_PULLUP);
  pinMode(dim7Pin, INPUT_PULLUP);
}

void loop() {
  // Read potentiometer
  int potVal = analogRead(potPin);  
  Serial.print(potVal);

  // Read button
  if (digitalRead(majPin)) {
    buttonState = 1; // Major
  } 
  else if (digitalRead(minPin)) {
    buttonState = 2; // Minor
  } 
  else if (digitalRead(dimPin)) {
    buttonState = 3; // Diminished
  } 
  else if (digitalRead(dom7Pin)) {
    buttonState = 4; // Dominant 7th
  } 
  else if (digitalRead(dim7Pin)) {
    buttonState = 5; // Minor 7th
  } 
  else {
    buttonState = 0; // No button pressed
  }

  Serial.print(potVal);
  Serial.print(",");
  Serial.println(buttonState);

  delay(10); // small delay to avoid flooding serial
}
