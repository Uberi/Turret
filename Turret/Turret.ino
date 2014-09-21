#include <Servo.h>

// use hardware PWM pins for output
const int yaw_pin = 9;
const int yaw_min = 10;
const int yaw_max = 170;

const int pitch_pin = 10;
const int pitch_min = 20;
const int pitch_max = 130;

const int trigger_pin = 11;
const int trigger_rest_angle = 100;
const int trigger_fire_angle = 160;

Servo yaw_servo;
Servo pitch_servo;
Servo trigger_servo;

void setup() {
  Serial.begin(9600);
  yaw_servo.attach(yaw_pin);
  yaw((yaw_min + yaw_max) / 2);
  pitch_servo.attach(pitch_pin);
  pitch((pitch_min + pitch_max) / 2);
  trigger_servo.attach(trigger_pin);
  trigger_servo.write(trigger_rest_angle);
}

void yaw(int angle) {
  yaw_servo.write(constrain(angle, yaw_min, yaw_max));
}

void pitch(int angle) {
  pitch_servo.write(constrain(angle, pitch_min, pitch_max));
}

void fire() {
  trigger_servo.write(trigger_fire_angle);
  delay(500);
  trigger_servo.write(trigger_rest_angle);
}

void loop() {
  while (Serial.available() > 0) {
    int command = Serial.read();
    if (command == 'f') {
      Serial.println("FIRING");
      fire();
    } else if (command == 'y') {
      int angle = Serial.parseInt();
      Serial.print("SETTING YAW TO "); Serial.println(angle);
      yaw(angle);
    }
    else if (command == 'p') {
      int angle = Serial.parseInt();
      Serial.print("SETTING PITCH TO "); Serial.println(angle);
      pitch(angle);
    }
    while (Serial.read() != '\n'); // consume characters up to and including the next newline
  }
}

