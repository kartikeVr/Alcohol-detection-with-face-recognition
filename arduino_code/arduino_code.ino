#include <MCUFRIEND_kbv.h>

MCUFRIEND_kbv tft;

#define MQ3_PIN A8 
#define esp8266 31 // Connect your MQ3 sensor to Analog pin A0
const int ledgre =49 ;
const int buzz=53;     // Digital pin connected to the LED
//const int ledred = 54;     // Digital pin connected to the LED
void setup() {
  pinMode(ledgre, OUTPUT);
  pinMode(buzz, OUTPUT);
  Serial.begin(9600);
 // pinMode(ledred, OUTPUT);

 // Cool transition element:
 uint16_t ID = tft.readID();
 tft.begin(ID);
 tft.setRotation(1);  // Adjust according to your screen orientation

 // Reveal "Alcohol Sensor" text with a wipe-in animation
 tft.fillScreen(TFT_BLACK);
 tft.setTextSize(4);
 tft.setTextColor(TFT_RED);
 tft.setCursor(40, 100);

 for (int i = 0; i < 17; i++) {
   tft.fillRect(0, 0, tft.width(), i * tft.height() /(15) , TFT_BLACK);  // Wipe screen from top to bottom
   tft.print("Alcohol Sensor");
   
   delay(50); 
 }

 tft.setTextSize(3);
 tft.setTextColor(0xFFFF, 0xF000);
 tft.setCursor(130, 0);
  
}

void loop() {

  int screenW = tft.width();  // Get screen width
  int screenH = tft.height();  // Get screen height
  tft.setTextColor(0xFFFF, 0x0000);

  int mq3_value = analogRead(MQ3_PIN);
  tft.setCursor(0,0);
  tft.setTextColor(TFT_CYAN);
  tft.print("Alcohol detection system");
  tft.setTextColor(0xFFFF, 0x0000);
  tft.setCursor(150, 140);
  tft.print("MQ3 Value: ");
  tft.println(mq3_value);
  if (mq3_value>350){
    Serial.println("Alcohol detected");
    //digitalWrite(ledred, HIGH); // Turn on the LED
    digitalWrite(buzz, HIGH);
    digitalWrite(esp8266, HIGH);
    tft.fillScreen(TFT_BLACK);
    tft.setTextSize(3);
    tft.setCursor(90,140);
    tft.setTextColor(TFT_RED, 0x0000);
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);    
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);    
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);    
    tft.print("ALERT!!! PERSON DRUNK");
    tft.setCursor(90,140);
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(100,140);
    tft.setTextColor(TFT_RED,TFT_BLACK);
    tft.println("The person is ");
    tft.setCursor(100,170);
    tft.println("extremely Drunk.");
    delay(2000);
    tft.setTextColor(TFT_BLACK,TFT_BLACK);
    tft.fillScreen(TFT_BLACK);


}
  else if(mq3_value>250 && mq3_value<350){

    tft.setCursor(100,140);
    tft.setTextColor(TFT_YELLOW,TFT_BLACK);
    tft.println("The person is mild.");
    tft.setCursor(110,170);
    tft.print("drunk.");
    digitalWrite(buzz, HIGH);
    digitalWrite(esp8266, HIGH);
    delay(2000);
    tft.setTextColor(TFT_BLACK,TFT_BLACK);
    tft.fillScreen(TFT_BLACK);

  }
  else{
    digitalWrite(ledgre, HIGH); // Turn on the LED
    tft.setCursor(150, 140);
    tft.print("MQ3 Value: ");
    tft.println(mq3_value);
    digitalWrite(buzz, LOW);
    digitalWrite(esp8266, LOW);

  }
  
  delay(1000);
}