#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  // DİKKAT: HIZI 12 KATINA ÇIKARDIK (Otoyol Hızı)
  Serial.begin(115200); 
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);
}

void loop() {
  if (Serial.available() > 0) {
    int motor = Serial.parseInt(); 
    int pwm_degeri = Serial.parseInt(); 

    if (Serial.read() == '\n') {
      if (motor >= 0 && motor <= 15 && pwm_degeri >= 100 && pwm_degeri <= 650) {
        pwm.setPWM(motor, 0, pwm_degeri);
        // Bütün Serial.print() satırlarını sildik. Arduino artık cevap vermekle vakit kaybetmeyecek.
      }
    }
  }
}