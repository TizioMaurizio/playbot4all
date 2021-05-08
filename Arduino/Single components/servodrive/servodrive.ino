/*
 Reads a SERVONUM sequence of 3 digits integers starting with s and ending with \n (like S090180150090090\n) and sets the angles on the servo drive (SDA -> A4, SCL -> A5)
 Message is received on softSerial on pins 10(RX) and 11(TX)
*/
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <SoftwareSerial.h>

#define SERVOMIN  125 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  575 // this is the 'maximum' pulse length count (out of 4096)
#define NONE -99

int SERVONUM = 16;
//int RECLEN = SERVONUM*3+1; //account for \n
//SoftwareSerial linkSerial(10, 11); // RX, TX
Servo myservo;  // for use without drive, signal on pin 9
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// MOTOR STARTING POSITIONS
int servos[16] = {90, 102, 121, 91, 80, 90, 90, 90, 90, 90, 90, 104, 95, 72, 73, 90};
//SERVO ARM
//Hand 'a' >=30
//Swing 'd' >=80

//Motor variables
int targetPoses[16] = {90, 102, 121, 91, 80, 90, 90, 90, 90, 90, 90, 104, 95, 72, 73, 90}; //from hand to swing
int velocities[16] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
unsigned long previousMillis = 0;
const long INTERVAL = 14; //1 degree every 17ms (about 60 degrees per second) --NOTE one cycle seems to take around 10ms, lowering the value under that is harmful for performance
int INCREMENT = 1; //change this to speed up movement once interval is minimized
unsigned long currentMillis = millis();
int deltaMove;
bool speedSet = false;

void setup() {
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  Serial.begin(9600);
  Serial.setTimeout(5);
  for(int i=0; i<16; i++){  // power motors to starting position
    pwm.setPWM(i, 0, angleToPulse(servos[i]));
    targetPoses[i] = servos[i];
  }
}

void loop() {
  currentMillis = millis();
  
  //read angles every INTERVAL milliseconds
  if(Serial.available()){
    //if(linkSerial.read() != 's')
    if(Serial.read() != 's')
      return 0;
    String serialResponse = Serial.readString();
    Serial.println(serialResponse);
    if(serialResponse.length() != RECLEN || serialResponse[RECLEN-1] != '\n'){
      Serial.println("Invalid string");
      return 0;
    }
    String str[SERVONUM] = {"","",""};
    for(int i=0; i<SERVONUM; i++){
      str[i] = "";
      for(int j=0; j<3; j++){
        str[i].concat(serialResponse[i*3+j]);
      }
    }
    for(int i=0; i<SERVONUM; i++){
      targetPoses[i] = str[i].toInt();
      //Serial.print(str[i]);
    }
  }
  
  //update motor pose every INTERVAL milliseconds
  unsigned long deltaT = currentMillis - previousMillis;
  if (deltaT >= INTERVAL) {
    previousMillis = currentMillis;
    if(deltaT - INTERVAL > 3)
      Serial.println(deltaT);
    for(int i=0; i<SERVONUM; i++){
      if(servos[i] != targetPoses[i]){
        deltaMove = targetPoses[i] - servos[i];
        if(abs(deltaMove) <= INCREMENT)
          servos[i] = targetPoses[i];
        else 
          servos[i] += INCREMENT * sign(deltaMove) * velocities[i];
        pwm.setPWM(i, 0, angleToPulse(servos[i]));
      }
    }
  }
}



int sign(int x){
  if (x > 0) return 1;
  if (x < 0) return -1;
  return 0;
}


/*
 * angleToPulse(int ang)
 * gets angle in degree and returns the pulse width
 * also prints the value on seial monitor
 * written by Ahmad Nejrabi for Robojax, Robojax.com
 */
int angleToPulse(int ang){
   int pulse = map(ang,0, 180, SERVOMIN,SERVOMAX);// map angle of 0 to 180 to Servo min and Servo max
   return pulse;
}
