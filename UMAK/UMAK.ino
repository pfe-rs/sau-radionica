/**
 * UMAK: Univerzalni Modularni Aparaturni Kontroler (za Arduino)
 * Original by Nikola Milenić, ported for Arduino by Luka Simić
 */

#include <Servo.h> 
#include "Adafruit_MCP9808.h"

// Types
typedef void (*actuator)(unsigned int);
typedef unsigned int (*sensor)(char);
typedef enum {
  STATE_INIT,
  STATE_BIND,
  STATE_BIND_OUT,
  STATE_BIND_OUT_DEVICE_CONFIG,
  STATE_BIND_IN,
  STATE_BIND_IN_SENSOR_PARAM,
  STATE_BIND_IN_DEVICE_CONFIG,
  STATE_ACT,
  STATE_ACT_READ_INPUT,
  STATE_SENSOR
} UMAKState;
typedef enum {
  DEVICE_OUT_DAC,
  DEVICE_OUT_PWM1,
  DEVICE_OUT_PWM2
} UMAKOutputDevice;
typedef enum {
  DEVICE_IN_ADC,
  DEVICE_IN_TEMP_SENSOR
} UMAKInputDevice;

// Channel configuration
actuator actuators[16] = {0};
sensor sensors[16] = {0};
char sensorParams[16] = {0};
char sensorBytes[16] = {0};
char actuatorBytes[16] = {0};

// Servo object representing the MG 996R servo
Servo servo1, servo2;

// Temperature sensor
Adafruit_MCP9808 tempsensor = Adafruit_MCP9808();

/**
 * Constants
 */
// Commands received as the first byte
const unsigned char CMD_SENSOR = 255;
const unsigned char CMD_ACT = 254;
const unsigned char CMD_BIND = 253;
// Device modes as the second byte during binding
const unsigned char BIND_IN = 252;
const unsigned char BIND_OUT = 251;

// State machine temporary
UMAKState state = STATE_INIT;
char channelId = 0;
unsigned bytesLeft = 0;
unsigned actInput = 0;
boolean DigitalTempSensor;

// Allows users to specify ports over 100 to target analog ports
int mapPort(char channel) {
  if (channel >= 100) {
    switch (channel) {
      case 100: return A0;
      case 101: return A1;
      case 102: return A2;
      case 103: return A3;
      case 104: return A4;
      case 105: return A5;
    }
  }
  return channel;
}

// Reports when an error occurs
void reportError() {
  Serial.write('E');
}

void reportAcknowledge() {
  Serial.write('A');
}

// Used for controlling servo motors
void servo1Actuator(unsigned int value) {
  servo1.write(value);
}

void servo2Actuator(unsigned int value) {
  servo2.write(value);
}

// Used for controlling the heater
void heaterActuator(unsigned int value) {
  analogWrite(11, value);
}

// Reads from ADC
unsigned int adcSensor(char channel) {
  return analogRead(mapPort(channel));
}

unsigned int digitalSensor(char chanel){
  tempsensor.readTempC();
}

void setup() {
  DigitalTempSensor = tempsensor.begin();
  Serial.begin(19200);
  servo1.attach(9);
  servo2.attach(10);
  delay(100);
}

void loop() {
  if (Serial.available() == 0) {
    // No data available
    return;
  }
  int uartByte = Serial.read();
  switch (state) {
    // Determining which command we received
    case STATE_INIT:
      switch (uartByte) {
        case CMD_BIND:
          state = STATE_BIND;
          break;
        case CMD_ACT:
          state = STATE_ACT;
          break;
        case CMD_SENSOR:
          state = STATE_SENSOR;
          break;
        default:
          reportError();
          break;
      }
      break;
    // Read device mode for configuration
    case STATE_BIND:
      switch (uartByte) {
        case BIND_OUT:
          state = STATE_BIND_OUT;
          break;
        case BIND_IN:
          state = STATE_BIND_IN;
          break;
        default:
          reportError();
          break;
      }
      break;
    // Read channel ID for configuring an output device
    case STATE_BIND_OUT:
      channelId = uartByte;
      state = STATE_BIND_OUT_DEVICE_CONFIG;
      break;
    // Configure which output device to use on the channel
    // Ends the BIND command (OUT option)
    case STATE_BIND_OUT_DEVICE_CONFIG:
      switch (uartByte) {
        case DEVICE_OUT_DAC:
          actuators[channelId] = heaterActuator;
          actuatorBytes[channelId] = 2;
          reportAcknowledge();
          break;
        case DEVICE_OUT_PWM1:
          actuators[channelId] = servo1Actuator;
          actuatorBytes[channelId] = 1;
          reportAcknowledge();
          break;
        case DEVICE_OUT_PWM2:
          actuators[channelId] = servo2Actuator;
          actuatorBytes[channelId] = 1;
          reportAcknowledge();
          break;
        default:
          reportError();
          break;
      }
      state = STATE_INIT;
      break;
    // Read channel ID for configuring an input device.
    case STATE_BIND_IN:
      channelId = uartByte;
      state = STATE_BIND_IN_SENSOR_PARAM;
      break;
    // Read sensor parameter for configuring an input device
    case STATE_BIND_IN_SENSOR_PARAM:
      sensorParams[channelId] = uartByte;
      state = STATE_BIND_IN_DEVICE_CONFIG;
      break;
    // Configure which input device to use on the channel
    // Ends the BIND command (IN option)
    case STATE_BIND_IN_DEVICE_CONFIG:
      switch (uartByte) {
        case DEVICE_IN_ADC:
          sensors[channelId] = adcSensor;
          sensorBytes[channelId] = 2;
          reportAcknowledge();
          break;
        case DEVICE_IN_TEMP_SENSOR:
          if (!DigitalTempSensor) {
            reportError();
            break;
          }
          sensors[channelId] = digitalSensor;
          sensorBytes[channelId] = 2;
          reportAcknowledge();
          break;
        default:
          reportError();
          break;
      }
      state = STATE_INIT;
      break;
    // Reads channel ID and configures parameters for writing to device
    case STATE_ACT:
      channelId = uartByte;
      bytesLeft = actuatorBytes[channelId];
      if (bytesLeft == 0) {
        // Channel not configured
        reportError();
        state = STATE_INIT;
      } else {
        actInput = 0;
        state = STATE_ACT_READ_INPUT;
      }
      break;
    // Reads input argument and sends it to actuator
    // Ends the ACT command
    case STATE_ACT_READ_INPUT:
      actInput *= 256;
      actInput += uartByte;
      if (--bytesLeft == 0) {
        actuators[channelId](actInput);
        reportAcknowledge();
        state = STATE_INIT;
      }
      break;
    // Reads channel ID for the sensor and returns configured sensor data
    case STATE_SENSOR:
      channelId = uartByte;
      bytesLeft = sensorBytes[channelId];
      if (bytesLeft == 0) {
        // Channel not configured
        reportError();
      } else {
        // Begin sensor data
        Serial.write('S');
        unsigned output = sensors[channelId](sensorParams[channelId]);
        for (; bytesLeft > 0; --bytesLeft) {
          Serial.write(output % 256);
          output /= 256;
        }
      }
      state = STATE_INIT;
      break;
  }
}
