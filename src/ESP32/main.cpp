#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#define POTPIN 34  // Pino do potenciômetro

Adafruit_MPU6050 mpu;

float last_accel_x, last_accel_y, last_accel_z;
bool first_reading = true;

// Limiar de vibração. Se a mudança na aceleração for maior que este valor, consideramos vibração.
const float LIMIAR_VIBRACAO = 2.5; 

void setup() {
  Serial.begin(115200);

  while (!Serial) delay(10);  // Aguarda o Serial conectar

  // Inicia o sensor MPU6050
  if (!mpu.begin()) {
    Serial.println("Falha ao encontrar o chip MPU6050. Verifique as conexões!");
    while (1) {
      delay(10);
    }
  }

  Serial.println("Sensor MPU6050 encontrado!");

  // Configura a faixa de medição do acelerômetro
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);  // Opções: 2_G, 4_G, 8_G, 16_G
  delay(100);
}

void loop() {
  delay(2000);

  float amper = analogRead(POTPIN) / 100.0;  // Converte o valor para uma faixa simulada de corrente

  // Obtém os eventos do MPU6050 (aceleração, giroscópio e temperatura)
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  // Na primeira leitura, apenas armazenamos os valores iniciais
  if (first_reading) {
    last_accel_x = accel.acceleration.x;
    last_accel_y = accel.acceleration.y;
    last_accel_z = accel.acceleration.z;
    first_reading = false;
    return;
  }

  // Calcula a diferença absoluta entre a leitura atual e a anterior
  float delta_x = abs(accel.acceleration.x - last_accel_x);
  float delta_y = abs(accel.acceleration.y - last_accel_y);
  float delta_z = abs(accel.acceleration.z - last_accel_z);

  // Calcula a magnitude da mudança
  float magnitude_variacao = delta_x + delta_y + delta_z;

  // Imprime a magnitude para calibração
  Serial.print("Magnitude da Variação: ");
  Serial.println(magnitude_variacao);

  // Verifica se a magnitude ultrapassou o limiar
  if (magnitude_variacao > LIMIAR_VIBRACAO) {
    Serial.println(">> VIBRAÇÃO DETECTADA! <<");
  }

  if (isnan(amper)) {
    Serial.println("Falha ao ler o Potenciometro!");
    return;
  }

  // Atualiza os valores da última leitura
  last_accel_x = accel.acceleration.x;
  last_accel_y = accel.acceleration.y;
  last_accel_z = accel.acceleration.z;

  // Exibe a temperatura do MPU6050
  Serial.print("Temperatura (MPU6050): ");
  Serial.print(temp.temperature);
  Serial.println(" *C");

  // Exibe a corrente simulada
  Serial.print("Corrente: ");
  Serial.print(amper);
  Serial.println(" A");
}