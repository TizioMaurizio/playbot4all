//INDEX: (ctrl+F, check capital letters)

////////JSON state manager
//Led r:11*,g:10,b:9,2
//Button 
//Capacitive 8
//Analog x:A0,y:A1
//Rotary sw:3,dt:4,clk:5
//IMU A4**, A5

////////Locomotion manager
//IR Sensor 12,13
//ServoDrive A4, A5

//*assigned pins
//**I2C: SDA A4, SCL A5
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//begin
//defines for serial debugging
#define LED_SERIAL false
#define BUTTON_SERIAL false
#define CAPACITIVE_SERIAL false
#define ANALOG_SERIAL false
#define ROTARY_SERIAL false
#define IMU_SERIAL false
#define IR_SERIAL false
#define SERVODRIVE_SERIAL false

#define UPDATE_TIME 50 //milliseconds

#include <ArduinoJson.h>

int componentsAmount = 0;
int toUpdate = 0; //see below
//setup functions bring this up to the amount of components,
//everytime a component updates its field in the JSON it decreases this value by one,
//this gets refreshed to the total amount of components whenever UPDATE_TIME exprires

// Allocate the JSON document
//
// Inside the brackets, 200 is the RAM allocated to this document.
// Don't forget to change this value to match your requirement.
// Use arduinojson.org/v6/assistant to compute the capacity.
StaticJsonDocument<200> JSON;
// StaticJsonObject allocates memory on the stack, it can be
// replaced by DynamicJsonDocument which allocates in the heap.
//
// DynamicJsonDocument  doc(200);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////JSON state manager
////////JSON state manager
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Led
//Led
int LED_red_light_pin= 11;
int LED_green_light_pin = 10;
int LED_blue_light_pin = 9;
int LED_prev_state = 0;
int LED_color = 0; //module 8 gets the color
#define RED {255,0,0}
int LED_colors[8][3] = {RED,{0,255,0},{0,0,255},{255,255,125},{0,255,255},{255,0,255},{255,255,0},{255,255,255}};
int LED_pushButton = 2;

void LED_setup(){
  pinMode(LED_red_light_pin, OUTPUT);
  pinMode(LED_green_light_pin, OUTPUT);
  pinMode(LED_blue_light_pin, OUTPUT);
  // initialize serial communication at 9600 bits per second:
  // make the pushbutton's pin an input:
  pinMode(LED_pushButton, INPUT);
  if(LED_SERIAL){
    Serial.println("-LED");
  }
  componentsAmount++;
}

void LED_loop(){
  // read the input pin:
  int LED_button_state = digitalRead(LED_pushButton);
  
  if(LED_prev_state != LED_button_state && LED_button_state == 1){
    LED_color++;
    LED_RGB_color(LED_colors[LED_color%8][0], LED_colors[LED_color%8][1], LED_colors[LED_color%8][2]);
  }
  if(LED_SERIAL){
    // print out the state of the button:
    Serial.println(LED_button_state);
  }
  LED_prev_state = LED_button_state; 
  
  if(toUpdate--){
    //update JSON
  }
}

void LED_RGB_color(int LED_red_light_value, int LED_green_light_value, int LED_blue_light_value)
 {
  analogWrite(LED_red_light_pin, LED_red_light_value);
  analogWrite(LED_green_light_pin, LED_green_light_value);
  analogWrite(LED_blue_light_pin, LED_blue_light_value);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Button
//Button
bool BUTTON_btn[4];

void BUTTON_setup(){
  
  componentsAmount++;
}

void BUTTON_loop(){
  
  if(toUpdate--){
    //update JSON
    /*JSON["button"]["top"] = BUTTON_btn[0];
    JSON["button"]["right"] = BUTTON_btn[1];
    JSON["button"]["left"] = BUTTON_btn[2];
    JSON["button"]["back"] = BUTTON_btn[3];*/
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Capacitive
//Capacitive
#define CAPACITIVE_touchpin 8 // sets the capactitive touch sensor @pin 4

bool CAPACITIVE_already = false;
bool CAPACITIVE_detected = false;
//int CAPACITIVE_ledPin = 2; // sets the LED @pin 2
void CAPACITIVE_setup() {
  pinMode(CAPACITIVE_touchpin, INPUT); //sets the touch sensor as input
  //pinMode(CAPACITIVE_ledPin, OUTPUT);  //sets the led as output
  if(CAPACITIVE_SERIAL){
    Serial.println("-Capacitive Touch Sensor");
  }
  componentsAmount++;
}
void CAPACITIVE_loop() {
  int CAPACITIVE_touchValue = digitalRead(CAPACITIVE_touchpin); //reads the touch sensor signal
  if (CAPACITIVE_touchValue == HIGH){      //if sensor is HIGH
    //digitalWrite(CAPACITIVE_ledPin, HIGH);   //LED will turn ON
    CAPACITIVE_detected = true;
    //testing
    //digitalWrite(IR_LED, HIGH); // LED High
    if(CAPACITIVE_detected && !CAPACITIVE_already){
      if(CAPACITIVE_SERIAL){
        Serial.println("Capacitive: touch detected");
      }
    }
    CAPACITIVE_already = true;
  }
  else{       //otherwise
    CAPACITIVE_detected = false;
    CAPACITIVE_already = false;
    //digitalWrite(CAPACITIVE_ledPin,LOW); //LED is turned OFF
  }
  
  if(toUpdate--){
    //update JSON
    JSON["capacitive"] = CAPACITIVE_detected;
  } 
  //delay(300);   //delay of 300milliseconds
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Analog
//Analog
#define ANALOG_joyX A0
#define ANALOG_joyY A1

void ANALOG_setup() {
  if(ANALOG_SERIAL){
    Serial.println("-Analog Stick");
  }
  componentsAmount++;
}
 
void ANALOG_loop() {
  // put your main code here, to run repeatedly:
  int ANALOG_xValue = analogRead(ANALOG_joyX);
  int ANALOG_yValue = analogRead(ANALOG_joyY);
 
  //print the values with to plot or view
  if(ANALOG_xValue < 500 || ANALOG_yValue < 500 || ANALOG_xValue > 510 || ANALOG_yValue > 510){ //INTRODUCES DEAD ZONE ON JOYSTICK
    if(ANALOG_SERIAL){
      Serial.print(ANALOG_xValue);
      Serial.print("\t");
      Serial.println(ANALOG_yValue);
    }
  }
  
  if(toUpdate--){
    //update JSON
    JSON["analog"]["x"] = ANALOG_xValue;
    JSON["analog"]["y"] = ANALOG_yValue;
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Rotary
//Rotary
// Rotary Encoder Inputs
#define ROTARY_CLK 5
#define ROTARY_DT 3
#define ROTARY_SW 4
 
int ROTARY_counter = 0;
int ROTARY_currentStateCLK;
int ROTARY_lastStateCLK;
String ROTARY_currentDir ="";
unsigned long ROTARY_lastButtonPress = 0;
 
void ROTARY_setup() {
  
  // Set encoder pins as inputs
  pinMode(ROTARY_CLK,INPUT);
  pinMode(ROTARY_DT,INPUT);
  pinMode(ROTARY_SW, INPUT_PULLUP);
 
  // Read the initial state of CLK
  ROTARY_lastStateCLK = digitalRead(ROTARY_CLK);
  if(ROTARY_SERIAL){
    Serial.println("-Rotary Encoder");
  }
  componentsAmount++;
}
 
void ROTARY_loop() {
  
  // Read the current state of CLK
  ROTARY_currentStateCLK = digitalRead(ROTARY_CLK);
 
  // If last and current state of CLK are different, then pulse occurred
  // React to only 1 state change to avoid double count
  if (ROTARY_currentStateCLK != ROTARY_lastStateCLK  && ROTARY_currentStateCLK == 1){
 
    // If the DT state is different than the CLK state then
    // the encoder is rotating CCW so decrement
    if (digitalRead(ROTARY_DT) != ROTARY_currentStateCLK) {
      ROTARY_counter --;
      ROTARY_currentDir ="CCW";
    } else {
      // Encoder is rotating CW so increment
      ROTARY_counter ++;
      ROTARY_currentDir ="CW";
    }
    if(ROTARY_SERIAL){
      Serial.print("Direction: ");
      Serial.print(ROTARY_currentDir);
      Serial.print(" | Counter: ");
      Serial.println(ROTARY_counter);
    }
  }
 
  // Remember last CLK state
  ROTARY_lastStateCLK = ROTARY_currentStateCLK;
 
  // Read the button state
  int ROTARY_btnState = digitalRead(ROTARY_SW);
 
  //If we detect LOW signal, button is pressed
  if (ROTARY_btnState == LOW) {
    //if 50ms have passed since last LOW pulse, it means that the
    //button has been pressed, released and pressed again
    if(ROTARY_SERIAL){
      if (millis() - ROTARY_lastButtonPress > 50) {
        Serial.println("Button pressed!");
      }
    }
 
    // Remember last button press event
    ROTARY_lastButtonPress = millis();
  }
  
  if(toUpdate--){
    //update JSON
    JSON["rotary"] = ROTARY_counter;
  }
 
  // Put in a slight delay to help debounce the reading
  //delay(1);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////IMU
//IMU
// MPU-6050 Short Example Sketch
// By Arduino User JohnChi
// August 17, 2014
// Public Domain
#include<Wire.h>
const int IMU_MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t IMU_AcX,IMU_AcY,IMU_AcZ,IMU_Tmp,IMU_GyX,IMU_GyY,IMU_GyZ;
void IMU_setup(){
  Wire.begin();
  Wire.beginTransmission(IMU_MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  if(IMU_SERIAL){
    Serial.println("-IMU");
  }
  componentsAmount++;
}
void IMU_loop(){
  Wire.beginTransmission(IMU_MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(IMU_MPU_addr,14,true);  // request a total of 14 registers
  IMU_AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  IMU_AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  IMU_AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  IMU_Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  IMU_GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  IMU_GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  IMU_GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  
  if(IMU_SERIAL){
    if (false){
      Serial.print("AcX = "); Serial.print(IMU_AcX);
      Serial.print(" | AcY = "); Serial.print(IMU_AcY);
      Serial.print(" | AcZ = "); Serial.print(IMU_AcZ);
      Serial.print(" | Tmp = "); Serial.print(IMU_Tmp/340.00+36.53);  //equation for temperature in degrees C from datasheet
      Serial.print(" | GyX = "); Serial.print(IMU_GyX);
      Serial.print(" | GyY = "); Serial.print(IMU_GyY);
      Serial.print(" | GyZ = "); Serial.println(IMU_GyZ);
    }
    if(IMU_AcZ > -14000){ //detect vertical movement or inclination (imu pins facing down)
      Serial.print(" | AcZ = "); Serial.print(IMU_AcZ);
    }
  }
  
  if(toUpdate--){
    //update JSON
    JSON["imu"]["x"] = IMU_AcX;
    JSON["imu"]["y"] = IMU_AcY;
    JSON["imu"]["z"] = IMU_AcZ;
    //gyro?
  }
  //delay(333);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Locomotion manager
////////Locomotion manager
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////IR Sensor
//IR Sensor
int IR_IRSensor = 12; // connect ir sensor to arduino pin 2
bool IR_detected = false;
bool IR_already = false;
//int IR_LED = 13; // conect Led to arduino pin 13

void IR_setup() 
{
  pinMode (IR_IRSensor, INPUT); // sensor pin INPUT
  //pinMode (IR_LED, OUTPUT); // Led pin OUTPUT
  if(IR_SERIAL){
    Serial.println("-IR Sensor");
  }
  componentsAmount++;
}

void IR_loop()
{
  int IR_statusSensor = digitalRead (IR_IRSensor);
  
  if (IR_statusSensor == 1){
    IR_detected = false;
    IR_already = false; //to be sure
    //digitalWrite(IR_LED, LOW); // LED LOW
    //if(IR_SERIAL){
      //Serial.print("IR sensor: ");
      //Serial.println(IR_statusSensor);
    //}
  }
  
  else
  {
    IR_detected = true;
    //testing
    //digitalWrite(IR_LED, HIGH); // LED High
    if(IR_detected && !IR_already){
      if(IR_SERIAL){
        Serial.println("IR_Sensor: obstacle detected");
      }
    }
    IR_already = true;
  }
  
  if(toUpdate--){
    //update JSON
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////ServoDrive
//ServoDrive
/*
 Reads a SERVONUM sequence of 3 digits integers starting with s and ending with \n (like S090180150090090\n) and sets the angles on the servo drive (SDA -> A4, SCL -> A5)
 Message is received on softSerial on pins 10(RX) and 11(TX)
*/
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <SoftwareSerial.h>

#define SERVO_SERVOMIN  125 // this is the 'minimum' pulse length count (out of 4096)
#define SERVO_SERVOMAX  575 // this is the 'maximum' pulse length count (out of 4096)
#define SERVO_NONE -99

int SERVO_SERVONUM = 4;
int SERVO_RECLEN = SERVO_SERVONUM*3+1; //account for \n
//SoftwareSerial linkSerial(10, 11); // RX, TX
Servo SERVO_myservo;  // for use without drive, signal on pin 9
Adafruit_PWMServoDriver SERVO_pwm = Adafruit_PWMServoDriver();

// MOTOR STARTING POSITIONS
int SERVO_servos[16] = {90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90};
//SERVO ARM
//Hand 'a' >=30
//Swing 'd' >=80

//Motor variables
int SERVO_targetPoses[16] = {90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90}; //from hand to swing
int SERVO_velocities[16] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
unsigned long SERVO_previousMillis = 0;
const long SERVO_INTERVAL = 14; //1 degree every 17ms (about 60 degrees per second) --NOTE one cycle seems to take around 10ms, lowering the value under that is harmful for performance
int SERVO_INCREMENT = 1; //change this to speed up movement once interval is minimized
unsigned long SERVO_currentMillis = millis();
int SERVO_deltaMove;
bool SERVO_speedSet = false;

void SERVO_setup() {
  SERVO_pwm.begin();
  SERVO_pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  for(int i=0; i<SERVO_SERVONUM; i++){  // power motors to starting position
    SERVO_pwm.setPWM(i, 0, angleToPulse(SERVO_servos[i]));
    SERVO_targetPoses[i] = SERVO_servos[i];
  }
}

void SERVO_loop() {
  //read angles every INTERVAL milliseconds
  if(toUpdate--){
    for(int i=0; i<SERVO_SERVONUM; i++){
      SERVO_targetPoses[i] = JSON["servoangles"][i];
      SERVO_velocities[i] = JSON["servovelocities"][i];
    }
  }
  
  //update motor pose every INTERVAL milliseconds
  unsigned long SERVO_deltaT = SERVO_currentMillis - SERVO_previousMillis;
  if (SERVO_deltaT >= SERVO_INTERVAL) {
    SERVO_previousMillis = millis();
    SERVO_targetPoses[0] = JSON["servo"]["hip_right"];
    SERVO_targetPoses[1] = JSON["servo"]["leg_right"];
    SERVO_targetPoses[2] = JSON["servo"]["hip_left"];
    SERVO_targetPoses[3] = JSON["servo"]["leg_left"];
    if(SERVO_deltaT - SERVO_INTERVAL > 3)
      Serial.println(SERVO_deltaT);
    for(int i=0; i<SERVO_SERVONUM; i++){
      if(SERVO_servos[i] != SERVO_targetPoses[i]){
        SERVO_deltaMove = SERVO_targetPoses[i] - SERVO_servos[i];
        if(abs(SERVO_deltaMove) <= SERVO_INCREMENT)
          SERVO_servos[i] = SERVO_targetPoses[i];
        else 
          SERVO_servos[i] += SERVO_INCREMENT * sign(SERVO_deltaMove) * SERVO_velocities[i];
        SERVO_pwm.setPWM(i, 0, angleToPulse(SERVO_servos[i]));
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
int angleToPulse(int SERVO_ang){
   int SERVO_pulse = map(SERVO_ang,0, 180, SERVO_SERVOMIN,SERVO_SERVOMAX);// map angle of 0 to 180 to Servo min and Servo max
   return SERVO_pulse;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//main

int prevTime = millis();

void setup() {
  // put your setup code here, to run once:
  //REMINDER initialize Serial only once
  Serial.begin(9600);
  Serial.println("Claudia's friend v0.01, print sensors on change, press buttons to change led color. (check the cables)");
  Serial.println("The purpose of this prototype is to acquire data from sensors and store them\ninto a JSON to be sent to Raspberry, also to read such JSON and actuate things accordingly.\nYou can enable or disable the prints of each sensor by editing the defines\nat the beginning of the code");
  Serial.println("\nEnabled serial prints:");
  LED_setup();
  BUTTON_setup();
  CAPACITIVE_setup();
  ANALOG_setup();
  ROTARY_setup();
  //IMU_setup();
  IR_setup();
  //SERVO_setup();
  Serial.print(componentsAmount);
  Serial.println(" components reflected by JSON");
}

void loop() {
  LED_loop();
  BUTTON_loop();
  CAPACITIVE_loop();
  ANALOG_loop();
  ROTARY_loop();
  //IMU_loop();
  IR_loop();
  //SERVO_loop();
  
  //JSON fields are filled in the functions' loops, then sent via serial every 50ms
  int currTime = millis();
  if(currTime - prevTime >= UPDATE_TIME){
    read_json();
    toUpdate = componentsAmount; //reduced by one in each loop function
    serializeJson(JSON, Serial);
    prevTime = millis();
  }
}

void read_json(){
  if(Serial.available() > 0){
    String inData = Serial.readStringUntil('\n');
    StaticJsonDocument<200> received;
    // Deserialize the JSON document
    DeserializationError error = deserializeJson(received, inData);
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }
    // Fetch values.
    //
    // Most of the time, you can rely on the implicit casts.
    // In other case, you can do received["time"].as<long>();
    JSON["led"]["top"] = received["led"]["top"];
    JSON["led"]["right"] = received["led"]["right"];
    JSON["led"]["left"] = received["led"]["left"];
    JSON["led"]["back"] = received["led"]["back"];
    JSON["servo"]["hip_right"] = received["servo"]["hip_right"];
    JSON["servo"]["leg_right"] = received["servo"]["leg_right"];
    JSON["servo"]["hip_left"] = received["servo"]["hip_left"];
    JSON["servo"]["leg_left"] = received["servo"]["leg_left"];
    // Print values.
  }
}
