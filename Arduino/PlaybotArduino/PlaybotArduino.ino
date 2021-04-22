//INDEX: (ctrl+F, check capital letters)

////////JSON state manager
//Led
//Button
//Capacitive
//Analog
//Rotary
//IMU

////////Locomotion manager
//IR Sensor
//ServoDrive

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//begin

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////JSON state manager
////////JSON state manager
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Led
//Led
int LED_red_light_pin= 11;
int LED_green_light_pin = 10;
int LED_blue_light_pin = 9;
int LED_prev_state = 0;
int LED_color = 0; //module 8 gets the color
int LED_colors[8][3] = {{255,0,0},{0,255,0},{0,0,255},{255,255,125},{0,255,255},{255,0,255},{255,255,0},{255,255,255}};
int LED_pushButton = 2;

void LED_setup(){
  pinMode(LED_red_light_pin, OUTPUT);
  pinMode(LED_green_light_pin, OUTPUT);
  pinMode(LED_blue_light_pin, OUTPUT);
  // initialize serial communication at 9600 bits per second:
  // make the pushbutton's pin an input:
  pinMode(LED_pushButton, INPUT);
}

void LED_loop(){
  // read the input pin:
  int LED_button_state = digitalRead(LED_pushButton);
  
  if(LED_prev_state != LED_button_state && LED_button_state == 1){
    LED_color++;
    LED_RGB_color(LED_colors[LED_color%8][0], LED_colors[LED_color%8][1], LED_colors[LED_color%8][2]);
  }
  // print out the state of the button:
  Serial.println(LED_button_state);
  LED_prev_state = LED_button_state; 
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

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Capacitive
//Capacitive


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Analog
//Analog
#define ANALOG_joyX A0
#define ANALOG_joyY A1

void ANALOG_setup() {
}
 
void ANALOG_loop() {
  // put your main code here, to run repeatedly:
  int ANALOG_xValue = analogRead(ANALOG_joyX);
  int ANALOG_yValue = analogRead(ANALOG_joyY);
 
  //print the values with to plot or view
  Serial.print(ANALOG_xValue);
  Serial.print("\t");
  Serial.println(ANALOG_yValue);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Rotary
//Rotary
// Rotary Encoder Inputs
#define ROTARY_CLK 2
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
 
    Serial.print("Direction: ");
    Serial.print(ROTARY_currentDir);
    Serial.print(" | Counter: ");
    Serial.println(ROTARY_counter);
  }
 
  // Remember last CLK state
  ROTARY_lastStateCLK = ROTARY_currentStateCLK;
 
  // Read the button state
  int ROTARY_btnState = digitalRead(ROTARY_SW);
 
  //If we detect LOW signal, button is pressed
  if (ROTARY_btnState == LOW) {
    //if 50ms have passed since last LOW pulse, it means that the
    //button has been pressed, released and pressed again
    if (millis() - ROTARY_lastButtonPress > 50) {
      Serial.println("Button pressed!");
    }
 
    // Remember last button press event
    ROTARY_lastButtonPress = millis();
  }
 
  // Put in a slight delay to help debounce the reading
  delay(1);
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
  Serial.print("AcX = "); Serial.print(IMU_AcX);
  Serial.print(" | AcY = "); Serial.print(IMU_AcY);
  Serial.print(" | AcZ = "); Serial.print(IMU_AcZ);
  Serial.print(" | Tmp = "); Serial.print(IMU_Tmp/340.00+36.53);  //equation for temperature in degrees C from datasheet
  Serial.print(" | GyX = "); Serial.print(IMU_GyX);
  Serial.print(" | GyY = "); Serial.print(IMU_GyY);
  Serial.print(" | GyZ = "); Serial.println(IMU_GyZ);
  delay(333);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Locomotion manager
////////Locomotion manager
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////IR Sensor
//IR Sensor
int IR_IRSensor = 2; // connect ir sensor to arduino pin 2
int IR_LED = 13; // conect Led to arduino pin 13

void setup() 
{
  pinMode (IR_IRSensor, INPUT); // sensor pin INPUT
  pinMode (IR_LED, OUTPUT); // Led pin OUTPUT
}

void loop()
{
  int IR_statusSensor = digitalRead (IR_IRSensor);
  
  if (IR_statusSensor == 1){
    digitalWrite(IR_LED, LOW); // LED LOW
    Serial.println(IR_statusSensor);
  }
  
  else
  {
    //testing
    digitalWrite(IR_LED, HIGH); // LED High
    Serial.println(IR_statusSensor);
  }
  
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////ServoDrive
//ServoDrive


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//main

void setup() {
  // put your setup code here, to run once:
  //REMINDER initialize Serial only once
  Serial.begin(9600);
  LED_setup();
  ANALOG_setup();
  ROTARY_setup();
}

void loop() {
  // put your main code here, to run repeatedly:
  LED_loop();
  ANALOG_loop();
  ROTARY_loop();
}
