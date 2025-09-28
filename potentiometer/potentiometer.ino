int potPin = A0; // Potentiometer output connected to analog pin 3
int potVal = 0; // Variable to store the input from the potentiometer
int majPin = 2;
int minPin = 3;
int dimPin = 4;
int dom7Pin = 5;
int dim7Pin = 6;
int octDownPin = 12;
int octUpPin = 13;
int buttonState = 0;

void setup() {
  Serial.begin(115200);
  pinMode(majPin, INPUT_PULLUP);
  pinMode(minPin, INPUT_PULLUP);
  pinMode(dimPin, INPUT_PULLUP);
  pinMode(dom7Pin, INPUT_PULLUP);
  pinMode(dim7Pin, INPUT_PULLUP);
  pinMode(octDownPin, INPUT_PULLUP);
  pinMode(octUpPin, INPUT_PULLUP);
}

void loop() {
  // Read potentiometer
  int potVal = analogRead(potPin); 

  if (digitalRead(octDownPin) == LOW) {
    Serial.println("D");
  } 
  if (digitalRead(octUpPin) == LOW) {
    Serial.println("U");
  } 

  // Read button
  if (digitalRead(majPin) == LOW) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(1);
    delay(10); // small delay to avoid flooding serial
    } 
  else if (digitalRead(minPin) == LOW) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(2);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dimPin) == LOW) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(3);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dom7Pin) == LOW) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(4);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dim7Pin) == LOW) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(5);
    delay(10); // small delay to avoid flooding serial
  } 
  else {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(0);
    delay(10); // small delay to avoid flooding serial
  }
}
