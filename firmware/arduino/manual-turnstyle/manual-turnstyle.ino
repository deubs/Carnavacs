#include <ArduinoHttpClient.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <Ethernet.h>

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif

#include <hiduniversal.h>                  //Add to Oleg Mazurov code to Bar Code Scanner
#include <usbhub.h>
#include <avr/pgmspace.h>
#include <Usb.h>
#include <usbhub.h>
#include <avr/pgmspace.h>
#include <hidboot.h>
USB     Usb;
USBHub     Hub(&Usb);                                          //I enable this line
HIDUniversal      Hid(&Usb);                                  //Add this line so that the barcode scanner will be recognized, I use "Hid" below 

 

#define RELE  2
#define SW  4

String last = "";
String qr = "";

int ID = 0x79; //121 

LiquidCrystal_I2C lcd(0x3F, 16, 2); 

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, ID };
IPAddress ip(10, 42, 190, ID);

EthernetClient ethClient;

char server[] = "10.42.190.8";
String url = "/QR/MolReadQR.asp?qrCode=";

HttpClient client = HttpClient(ethClient, server, 80);

/* write text in lcd display */
void show(String l1, String l2 = "");
String getValue(String data, char separator, int index);
void openTurn(); 

class KbdRptParser : public KeyboardReportParser
{
        void PrintKey(uint8_t mod, uint8_t key);             // Add this line to print character in ASCII
protected:
  virtual void OnKeyDown  (uint8_t mod, uint8_t key);
  virtual void OnKeyPressed(uint8_t key);
};
 
void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key)  
{
    uint8_t c = OemToAscii(mod, key);
 
    if (c)
        OnKeyPressed(c);
}
 
/* what to do when symbol arrives */
void KbdRptParser::OnKeyPressed(uint8_t key)  
{
static uint32_t next_time = 0;      //watchdog
next_time = millis() + 200;  //reset watchdog
Serial.print( (char)key );      //Add char to print correct number in ASCII
};
 



/* default disp message */
void welcome(String l2 = "Bienvenido...") {
  show("Carnaval", l2);
}

KbdRptParser Prs;

void setup() {
  Ethernet.init(8);
  Serial.begin( 115200 );

  lcd.init();
  lcd.backlight();

  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, HIGH);
  pinMode(SW, INPUT);
  digitalWrite(SW, LOW);

  Ethernet.begin(mac, ip);
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    show("NO ETH!!");
    while (true)  
      delay(1); // do nothing
  }

  //check link if feat is available 
  if (Ethernet.hardwareStatus() != EthernetW5100) {
    Serial.println(Ethernet.linkStatus());
  
//    while (Ethernet.linkStatus() != LinkON) {
//      show("Red desconectada", "Reintentando...");
//      delay(1000);
//    }
  }
  
//  while (!client.connect(server, 80))  {
//    show("Error de red", "Reconectando...");
//    delay(1000);
//  }


  if (Usb.Init() == -1) {
    Serial.println("OSC did not start.");
    show("No hay lector");
    while(1)
      delay(1000);
  }

  delay( 200 );
  Hid.SetReportParser(0, (HIDReportParser*)&Prs);   
  welcome("Terminal: " + (String)ID);
}


String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void openTurn() {
  
  int timeout = 8000;

  /* unblock */
  digitalWrite(RELE, LOW);
  
  /*wait turn*/
  while (digitalRead(SW) != HIGH && timeout >0) {
    delay(100);
    timeout -= 100;
  }

  digitalWrite(RELE, HIGH);  
  welcome();
}
  
void loop() {
  
  Usb.Task();

}


/* write text in lcd display */
void show(String l1, String l2 = "") {
  lcd.clear();
  lcd.print(l1);
  if (!l1.length())
    return welcome();
  if (l2.length()) {
    lcd.setCursor(0, 1);
    lcd.print(l2);
  }
}
