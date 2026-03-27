#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);
  Serial.println("Arduino Saf PWM Icin Hazir!");
}

void loop() {
  if (Serial.available() > 0) {
    int motor = Serial.parseInt(); 
    int pwm_degeri = Serial.parseInt(); 

    if (Serial.read() == '\n') {
      // Gelen değer motor 0-15 arası ve PWM 100-650 arasıysa çalıştır
      if (motor >= 0 && motor <= 15 && pwm_degeri >= 100 && pwm_degeri <= 650) {
        pwm.setPWM(motor, 0, pwm_degeri);
        Serial.print("Basarili -> Motor: ");
        Serial.print(motor);
        Serial.print(" | Saf PWM: ");
        Serial.println(pwm_degeri);
      }
    }
  }
}