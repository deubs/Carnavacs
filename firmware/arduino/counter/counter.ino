#include <ArduinoHttpClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <Ethernet.h>

/**
   turnstyle ID
   starting from 0x64 (100) to 120 (78). to compose mac and ip address)
    (-----rocamora---------)    (----------- ayacucho ---------------)   (----------- maipu  ------------------)    (---P7--)       (---P8--)   (provee)
    100    101    102    103    104    105    106    107    108    109    110    111    112    113    114    115    116    117    118    119 -    120
   0x64 - 0x65 - 0x66 - 0x67 - 0x68 - 0x69 - 0x6A - 0x6B - 0x6C - 0x6D - 0x6E - 0x6F - 0x70 - 0x71 - 0x72 - 0x73 - 0x74 - 0x75 - 0x76 - 0x77 -  0x78
*/
int ID = 0x70;
#define SW  4       /* el 112 de rocamora usa el 5! */
#define SW_ACTIVE LOW

/*estandar 0x3F, lo usa el 103!!
molinetes 0x27*/       

LiquidCrystal_I2C lcd(0x27, 16, 2);
SoftwareSerial ss(2, 3);

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, ID };
IPAddress ip(10, 42, 190, ID);

EthernetClient ethClient;

char server[] = "10.42.190.8";
String url = "/QR/Count?qr=10324444";

HttpClient client = HttpClient(ethClient, server, 80);

#define TIMEOUT 5000
#define RELE  A1

#define BLOCK_ACTIVE HIGH

int turning = 0;

String last = "";
String qr = "";


/* write text in lcd display */
void show(String l1, String l2 = "");


/* default disp message */
void welcome(String l2 = "Bienvenido...") {
  show("Carnaval", l2);
}

void setup() {
  Ethernet.init(10);
  Serial.begin(9600);
  ss.begin(9600);
  lcd.init();
  lcd.backlight();

  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, !BLOCK_ACTIVE);

  pinMode(SW, INPUT);
  digitalWrite(SW, !SW_ACTIVE);
  

  Ethernet.begin(mac, ip);
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    show("NO ETH!!");
    while (true)
      delay(1); // do nothing
  }

  //check link if feat is available
  if (Ethernet.hardwareStatus() != EthernetW5100) {
    Serial.println(Ethernet.linkStatus());

    while (Ethernet.linkStatus() != LinkON) {
      show("Red desconectada", "Reintentando...");
      delay(1000);
    }
  }

  while (!client.connect(server, 80))  {
    show("Error de red", "Reconectando...");
    delay(1000);
  }

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
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}




// Check status of switch
// return true if switch is pressed
bool checkSwitch() {

    if (digitalRead(SW) == SW_ACTIVE && turning == 1) {
        return false;
    }

    if (digitalRead(SW) == SW_ACTIVE) {
        delay(200);
        turning = 1;
        return true;
    }
    turning = 0;
    return false;
}

void loop() {
  int err = 0;


    if (checkSwitch()) {
    
      err = client.get(url);
      if (err == 0) {
        int statusCode = client.responseStatusCode();
        String result = client.responseBody();
        String status = getValue(result, '#', 0);
        String l1 = getValue(result, '#', 1);
        String l2 = getValue(result, '#', 2);
  
        show(l1, l2);
  
      } else {
        show("Error del servidor", "Reintentando...");
        Serial.print("Getting response failed: ");
        Serial.println(err);
      }
    }
        

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
