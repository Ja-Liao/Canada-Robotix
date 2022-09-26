#define cellPin A0

int buttonPin = 12;
int oldButtonRead = 1;
int newButtonRead = 1;
bool transmittingData = false;

// 5000 mv / 1024 bits = 4.8828
const float voltageConverter = 4.88;

float counts = 0;
float mv = 0;
float power;
float resistance = 30000;

void setup()
{
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
}

void loop()
{
  newButtonRead = digitalRead(buttonPin);
  if(oldButtonRead == 0 && newButtonRead == 1)
  {
    transmittingData = !transmittingData;
  }
//  Serial.println("oldButtonRead = " + String(oldButtonRead));
//  Serial.println("newButtonRead = " + String(newButtonRead));
//  Serial.println("transmittingData = " + String(transmittingData));
  //    Serial.println("Button Pressed");
//    transmittingData = !transmittingData;
    counts = analogRead(cellPin);
//    Serial.println("Cell Counts: " + String(counts));

    mv = counts * voltageConverter;
//    Serial.println("Cell MV: " + String(mv));

    power = (pow((mv * 3 / 1000), 2) / resistance) * 1000;
    // Serial.println("Power = " + String(power) + " mW");
    Serial.println(power);
  if(transmittingData)
  {
    Serial.println("Button Pressed");
    transmittingData = false;
  }
  oldButtonRead = newButtonRead;
  delay(500);
}
