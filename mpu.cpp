#include <Wire.h>

const int MPU6050Address = 0x68; // MPU6050 I2C address
const int MPU6050AccelConfig = 0x1C;
const int MPU6050GyroConfig = 0x1B;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  
  // Initialize MPU6050
  Wire.beginTransmission(MPU6050Address);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0);    // Wake up the MPU6050 (set to 0)
  Wire.endTransmission();

  // Set accelerometer range (+/-2g)
  Wire.beginTransmission(MPU6050Address);
  Wire.write(MPU6050AccelConfig);
  Wire.write(0); // 0 = +/-2g
  Wire.endTransmission();

  // Set gyro range (+/-250 degrees/second)
  Wire.beginTransmission(MPU6050Address);
  Wire.write(MPU6050GyroConfig);
  Wire.write(0); // 0 = +/-250 degrees/second
  Wire.endTransmission();
}

void loop() {
  int16_t accelerometerX, accelerometerY, accelerometerZ;
  int16_t gyroscopeX, gyroscopeY, gyroscopeZ;
  
  // Read accelerometer and gyroscope data
  Wire.beginTransmission(MPU6050Address);
  Wire.write(0x3B); // Starting register for accelerometer data
  Wire.endTransmission();
  Wire.requestFrom(MPU6050Address, 14); // Read 14 bytes (accelerometer and gyroscope data)

  accelerometerX = (Wire.read() << 8 | Wire.read());
  accelerometerY = (Wire.read() << 8 | Wire.read());
  accelerometerZ = (Wire.read() << 8 | Wire.read());

  gyroscopeX = (Wire.read() << 8 | Wire.read());
  gyroscopeY = (Wire.read() << 8 | Wire.read());
  gyroscopeZ = (Wire.read() << 8 | Wire.read());

  // Convert raw values to real values (sensitivity scale factors apply)
  float accelX = accelerometerX / 16384.0; // +/-2g range
  float accelY = accelerometerY / 16384.0;
  float accelZ = accelerometerZ / 16384.0;

  float gyroX = gyroscopeX / 131.0; // +/-250 degrees/second range
  float gyroY = gyroscopeY / 131.0;
  float gyroZ = gyroscopeZ / 131.0;

  // Print the values to the Serial Monitor
  Serial.print("Accel X: ");
  Serial.print(accelX);
  Serial.print("\tAccel Y: ");
  Serial.print(accelY);
  Serial.print("\tAccel Z: ");
  Serial.print(accelZ);

  Serial.print("\tGyro X: ");
  Serial.print(gyroX);
  Serial.print("\tGyro Y: ");
  Serial.print(gyroY);
  Serial.print("\tGyro Z: ");
  Serial.println(gyroZ);

  delay(1000); // You can adjust the delay as needed
}
