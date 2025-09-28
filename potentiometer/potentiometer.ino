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
  pinMode(majPin, INPUT);
  pinMode(minPin, INPUT);
  pinMode(dimPin, INPUT);
  pinMode(dom7Pin, INPUT);
  pinMode(dim7Pin, INPUT);
}

void loop() {
  // Read potentiometer
  int potVal = analogRead(potPin);  

  // Read button
  if (digitalRead(majPin)) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(1);
    delay(10); // small delay to avoid flooding serial
    } 
  else if (digitalRead(minPin)) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(2);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dimPin)) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(3);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dom7Pin)) {
    Serial.print(potVal);
    Serial.print(",");
    Serial.println(4);
    delay(10); // small delay to avoid flooding serial
  } 
  else if (digitalRead(dim7Pin)) {
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
