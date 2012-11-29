//include the OneWire library
#include <OneWire.h> 
// include the LiquidCrystal library:
#include <LiquidCrystal.h>

// initialize the LCD library with the numbers of the interface pins
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
int ButtonVoltage = 0;
int ButtonPressed = 0;
int Backlight = 10;
int fadeValue = 255;

#define BUTTON_SELECT    5
#define BUTTON_LEFT      4
#define BUTTON_DOWN      3
#define BUTTON_UP        2
#define BUTTON_RIGHT     1
#define BUTTON_NONE      0

int DS18S20_Pin = 2; //DS18S20 Signal pin on digital 2
int target_temp= 0; // Target temp for the system
int heater_relay = 3 ; //digital pin for the relay controlling the heat
int newTemp = 0;
int system_state = 0; //controls on/off state of the system

//Temperature chip i/o
OneWire ds(DS18S20_Pin);  // on digital pin 2

void setup(void) {
  Serial.begin(9600);

  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.setCursor (0,0);
  lcd.print("Temp:");
  lcd.setCursor (0,1);
  lcd.print("SetT:");
  lcd.setCursor(13,1);
  lcd.print("OFF");  
  //seup relay
  digitalWrite(heater_relay, 0); //makes sure the relay is off before init
  pinMode(heater_relay, OUTPUT);  
}

void loop(void) {
//getting the temp from the DS18S20
  float temperature = getTemp();
  float temp_f = ((temperature * 1.8) + 32);
  //Serial.println(temp_f); //prints farenheight
  //Serial.println(temperature); //prints celcius
  
 //printing the values to the lcd screen
  if (system_state == 1) {
    lcd.setCursor(13,1);
    lcd.print("ON ");
  }
  else {
    lcd.setCursor(13,1);
    lcd.print("OFF");
  }
  lcd.setCursor (5,0);
  lcd.print(temp_f);
  lcd.print("    ");// spaces to over write any previous values.
  lcd.setCursor (5,1);
  lcd.print(target_temp);
  lcd.print("     ");// spaces to over write any previous values. 
  //delay(500); //just here to slow down the output so it is easier to read

 // getting input from the lcd buttons
 ButtonVoltage = analogRead(0);
 //Serial.println(ButtonVoltage);
 
// Observed values:
//     NONE:    1023
//     SELECT:  722
//     LEFT:    481 
//     DOWN:    308
//     UP:      132
//     RIGHT:   0

  if (ButtonVoltage > 800) ButtonPressed = BUTTON_NONE;    // No button pressed should be 1023
  else if (ButtonVoltage > 500) ButtonPressed = BUTTON_SELECT;   
  else if (ButtonVoltage > 400) ButtonPressed = BUTTON_LEFT;   
  else if (ButtonVoltage > 250) ButtonPressed = BUTTON_DOWN;   
  else if (ButtonVoltage > 100) ButtonPressed = BUTTON_UP; 
  else ButtonPressed = BUTTON_RIGHT;
  
  switch (ButtonPressed) {
  case BUTTON_SELECT:
              if (system_state == 1) { 
                system_state = 0;}
              else if (system_state == 0){
                system_state = 1;}
              delay(500); //to make reduce multiple presses of button
              break;
  case BUTTON_LEFT:
              target_temp = target_temp + 10;
              delay(500);
              break;
  case BUTTON_DOWN:
              target_temp = target_temp - 1;    
              delay(500);
              break;
  case BUTTON_UP:
              target_temp = target_temp + 1;
              delay(500);
              break; 
  case BUTTON_RIGHT:
              target_temp = 0;
              delay(500);
              break;
  case BUTTON_NONE:
              //do nothing
              break;
  }
  
 
//turn the heater_relay on or off
  if (system_state == 1) { 
     if (temp_f < target_temp && temperature > 0) { 
        digitalWrite(heater_relay, HIGH);}
   
     else {
        digitalWrite(heater_relay, LOW);
    }
  }
  else {digitalWrite(heater_relay, LOW);
}
//serial communicatin for remote opperation
  if (Serial.available() > 0 ) {
    char inByte = Serial.read();
    switch(inByte)
    {
    case 't': //new set temp
      target_temp = numberFromSerial();
      Serial.println("set temp is now: ");
      Serial.println(target_temp);
      break;
    case 'n'://turn sytem on
      system_state = 1; 
      Serial.println("the system is ON");
      break;
    case 'f':
      system_state = 0;
      Serial.println("the system is OFF");
      break;
    case 'd':
      if (system_state == 0){
        Serial.println("OFF");
      }
      Serial.print("probe temp:") ;
      Serial.println( temp_f);
      Serial.print("set temp:");
      Serial.println(target_temp);
      break;
    default:
      Serial.println(".Invalid command Received by Arduino");
    }
    Serial.flush();
  }
  
}

//void handleSerialCommunication(void){ 
//  if (Serial.available() > 0 )
//  {
//    char inByte = Serial.read();
//    switch(inByte)
//    {
//    case 't': //new set temp
//      newTemp = numberFromSerial();
//      break;
//    default:
//      Serial.println(".Invalid command Received by Arduino");
//    }
//    Serial.flush();
//  }
//}
 
int numberFromSerial(void)
{
  char numberString[8];
  unsigned char index=0;
  delay(10);
  while(Serial.available() > 0)
  {
    delay(10);
    numberString[index++]=Serial.read();
    if(index > 6)
    {
      break;
    }
  }
  numberString[index]=0;
  return atoi(numberString);
}






//****************************************
//
// subroutine for the digital temp senesor
//
//****************************************
float getTemp(){
  //returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
    //no more sensors on chain, reset search
    ds.reset_search();
    return -1000;
  }

  if ( OneWire::crc8( addr, 7) != addr[7]) {
    //Serial.println("CRC is not valid!");
    return -1000;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
    //Serial.print("Device is not recognized");
    return -1000;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE); // Read Scratchpad


  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;

  return TemperatureSum;

}

