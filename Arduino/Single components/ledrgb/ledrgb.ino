int red_light_pin= 11;
int green_light_pin = 10;
int blue_light_pin = 9;
int prev_state = 0;
int color = 0; //module 8 gets the color
int colors[8][3] = {{255,0,0},{0,255,0},{0,0,255},{255,255,125},{0,255,255},{255,0,255},{255,255,0},{255,255,255}};
int pushButton = 2;
void setup() {
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
}
void loop() {
  // read the input pin:
  int button_state = digitalRead(pushButton);
  
  if(prev_state != button_state && button_state == 1){
    color++;
    RGB_color(colors[color%8][0], colors[color%8][1], colors[color%8][2]);
  }
  // print out the state of the button:
  Serial.println(button_state);
  prev_state = button_state;
}
void RGB_color(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_pin, red_light_value);
  analogWrite(green_light_pin, green_light_value);
  analogWrite(blue_light_pin, blue_light_value);
}
