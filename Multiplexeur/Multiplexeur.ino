#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM9DS0.h>

int pinMultiplexA0 = 7; 	// Pin  7 du Flora  (#6) => A0 du multiplexeur
int pinMultiplexA1 = 9; 	// Pin  9 du Flora  (#9) => A1 du multiplexeur
int pinMultiplexA2 = 10; 	// Pin 10 du Flora (#10) => A2 du multiplexeur

// Les capteurs sont branchés sur les entrées 1, 2, 3, 5, 6 et 7 du multiplexeur
boolean valuesForA0[] = {false, false, false, true,  true,  true}; // Bit de poids fort
boolean valuesForA1[] = {false, true,  true,  false, true,  true};
boolean valuesForA2[] = {true,  false, true,  true,  false, true}; // Bit de poids faible

/* Assign a unique base ID for this sensor */   
Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0(1000);// Use I2C, ID #1000

#define LSM9DS0_XM_CS 10
#define LSM9DS0_GYRO_CS 9

#define LSM9DS0_SCLK 13
#define LSM9DS0_MISO 12
#define LSM9DS0_MOSI 11

void configureSensor(void)
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);
  
  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
}

void setup(void) 
{
  pinMode(pinMultiplexA0, OUTPUT); 
  pinMode(pinMultiplexA1, OUTPUT);     
  pinMode(pinMultiplexA2, OUTPUT);   
   
#ifndef ESP8266
  while (!Serial);
#endif
  Serial.begin(9600);
  Serial.println(F("LSM9DS0 9DOF Sensor Test")); Serial.println("");
  
  /* Initialise the sensor */
  if(!lsm.begin())
  {
    /* There was a problem detecting the LSM9DS0 ... check your connections */
    Serial.print(F("Ooops, no LSM9DS0 detected ... Check your wiring or I2C ADDR!"));
    while(1);
  }
  Serial.println(F("Found LSM9DS0 9DOF"));
  
  /* Setup the sensor gain and integration time */
  configureSensor();
  
  /* We're ready to go! */
  Serial.println("We're ready to go!");
}

void loop(void)
{  
  for(int i = 0; i < sizeof(valuesForA0); i++) {
    digitalWrite(pinMultiplexA0, valuesForA0[i] ? HIGH : LOW);
    digitalWrite(pinMultiplexA1, valuesForA1[i] ? HIGH : LOW);
    digitalWrite(pinMultiplexA2, valuesForA2[i] ? HIGH : LOW);

    /* Get a new sensor event */ 
    sensors_event_t accel, mag, gyro, temp;
  
    lsm.getEvent(&accel, &mag, &gyro, &temp); 
  
    // print out accelleration data
    Serial.print("Acceleration : "); Serial.println(i);
    Serial.print("X: "); Serial.println(accel.acceleration.x);
    Serial.print("Y: "); Serial.println(accel.acceleration.y);
    Serial.print("Z: "); Serial.println(accel.acceleration.z);
    // print out accelleration data
    Serial.println("Gyroscope : "); Serial.println(i);
    Serial.print("X: "); Serial.println(gyro.gyro.x);
    Serial.print("Y: "); Serial.println(gyro.gyro.y);
    Serial.print("Z: "); Serial.println(gyro.gyro.z);
   
  }

  delay(1000);
}
