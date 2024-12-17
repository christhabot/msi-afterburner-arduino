#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Adjust the I2C address if necessary
unsigned long lastTime = 0;
bool dataReceived = false;
bool typed = false;

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600); // Start serial communication for receiving data
}

void loop() {
  String data = "";

  if (Serial.available()) {
    data = Serial.readStringUntil('\n');
    lastTime = millis(); // Reset the timer when data is received
    dataReceived = true;
  }

  if (millis() - lastTime > 1000) { // If no data received for 1 second
    if (!dataReceived) {
      if(!typed)
      {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("python script");
        lcd.setCursor(0, 1);
        lcd.print("not connected");
        typed = true;
      }
    }
  } else if (dataReceived) {
    lcd.setCursor(0, 0);
    lcd.print(data.substring(0, 16)); // First 16 characters
    lcd.setCursor(0, 1);
    lcd.print(data.substring(16, 32)); // Next 16 characters
    dataReceived = false; // Reset dataReceived after displaying
    typed = false;
  }
}
