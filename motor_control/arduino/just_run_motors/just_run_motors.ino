#define in1A 2
#define in2A 4
#define enA 3
#define enB 6
#define in1B 5
#define in2B 7


void setup() {
  // Motor driver pin setup
  pinMode(enA, OUTPUT);
  pinMode(in1A, OUTPUT);
  pinMode(in2A, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1B, OUTPUT);
  pinMode(in2B, OUTPUT);
  
  // Serial setup
  Serial.begin(115200l);
  Serial.setTimeout(10000);  // turn off motors after 10s no input
}

void moveLeft(int pwm, bool dir) {
  analogWrite(enA, pwm);
  // delay(200);
  digitalWrite(in1A, dir);
  digitalWrite(in2A, !dir);
}

void moveRight(int pwm, bool dir) {
  analogWrite(enB, pwm);
  // delay(200);
  digitalWrite(in1B, dir);
  digitalWrite(in2B, !dir);
}

void loop()
{
    moveRight(206, 1);
    moveLeft(206, 1);
}
