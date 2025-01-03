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
int ID = 0x10;
/*estandar 0x3F, molinetes 0x27*/
LiquidCrystal_I2C lcd(0x27, 16, 2);
SoftwareSerial ss(2, 3);

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, ID };
IPAddress ip(192, 168, 40, ID);

EthernetClient ethClient;

char server[] = "192.168.40.250";
String url = "/QR/Read?qr=";

HttpClient client = HttpClient(ethClient, server, 80);

#define TIMEOUT 5000
#define RELE  A1
#define SW  4
#define SW_ACTIVE LOW

#define SWITCH_MODE 1

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
  Serial.println("init");
  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, HIGH);

  pinMode(SW, INPUT);
  digitalWrite(SW, !SW_ACTIVE);
  
  show("INIT");
  int eth = Ethernet.begin(mac);
  if (eth == 1)
    Serial.println("DHCP OK");
  else
    Serial.println("DHCP NOT OK");
  Serial.println(eth);
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
  Serial.println("Terminal");
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


/**
Abre el molinete. desactiva solenoide hasta que cumpla el timeout o se active switch 
que marca la vuelta.
1000 espera siempre. es el tiempo que le da a que empieza a pasar*/
void openTurn() {
  
  int timeout = TIMEOUT - 1500;

  /* unblock */
  digitalWrite(RELE, LOW);
  show("Adelante...");
  delay(1500);
  
  /*wait*/
    Serial.print("SW " );
    Serial.print(SW);
  while (digitalRead(SW) != SW_ACTIVE && timeout > 0) {
    delay(200);
    timeout -= 200;
     Serial.print("buu: ");
  }
  /* block */
  digitalWrite(RELE, HIGH);
  welcome();
}

void loop() {

  qr = "";
  char c;
  int err = 0;

  while (ss.available()) {
    c = ss.read();
    if (c == '\n' || c == '\r')
      break;
    qr += c;
  }

  if (qr != "")
    Serial.println(qr);

  if (qr.length() && qr != last) {
    err = client.get(url + qr);
    if (err == 0) {

      int statusCode = client.responseStatusCode();
      Serial.println(statusCode);
      String result = client.responseBody();
      String status = getValue(result, '#', 0);
      String l1 = getValue(result, '#', 1);
      String l2 = getValue(result, '#', 2);
      Serial.println(result);
      Serial.println(status);
      show(l1, l2);
      Serial.println(l1);
      Serial.println(l2);
      if (status == "OK") {
        openTurn();
      }
      last = qr;
    } else {
      Serial.print("Getting response failed: ");
      Serial.println(err);
    }
  } else {
    delay(100);
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
