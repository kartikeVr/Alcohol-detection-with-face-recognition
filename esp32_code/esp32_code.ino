#include <WiFi.h>

const char* ssid = "Redminote11";
const char* password = "12345678";
const char* serverAddress = "192.168.66.3";
const int serverPort = 81; // Default HTTP port, adjust if needed
const int signalPin = 4; // Replace with your ESP32 pin

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(signalPin, INPUT); // Set signal pin to input with pull-up resistor

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int signalValue = digitalRead(signalPin);

  if (signalValue == HIGH) { // HIGH signal detected (active-low logic)
    if (WiFi.status() == WL_CONNECTED) {
      if (!client.connected()) {
        reconnectToServer(); // Reconnect if necessary
      }

      if (client.connected()) {
        String message = "HIGH_SIGNAL"; // Customize message for Python script
        client.print("POST /main_video.py HTTP/1.1\n");
        client.print("Host: ");
        client.print(serverAddress);
        client.print(":");
        client.println(serverPort);
        client.print("Content-Type: application/x-www-form-urlencoded\n");
        client.print("Content-Length: ");
        client.println(message.length());
        client.println("Connection: close\n");
        client.println();
        client.println(message);
        client.stop(); // Close the connection after sending
        Serial.println("Signal sent to PC!");
      } else {
        Serial.println("Failed to send signal, client not connected.");
      }
    } else {
      Serial.println("ESP32 not connected to Wi-Fi.");
    }
  }

  delay(15000); // Adjust delay based on desired signal detection frequency
}

void reconnectToServer() {
  while (!client.connected()) {
    Serial.print("Reconnecting to server...");
    if (client.connect(serverAddress, serverPort)) {
      Serial.println("connected!");
    } else {
      Serial.println("failed.");
      delay(5000); // Wait for a few seconds before retrying
    }
  }
}
