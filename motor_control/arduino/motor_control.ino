#define in1A 7
#define in2A 8
#define enB 5
#define enA 9
#define in1B 2
#define in2B 4


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

void loop() {
  while (Serial.available()) {
    long int msg = Serial.parseInt();

    // Decompose msg (msd lllrrrd lsd (e.g. 1801802))
    int dirs = msg % 10;
    bool left_dir = 1, right_dir = 1;  // 0 -> back, 1 -> forward
    msg /= 10;
    switch (dirs) {
      case 0:
        break;
      case 1:
        right_dir = 0;
        break;
      case 2:
        left_dir = 0;
        break;
      case 3:
        left_dir = 0;
        right_dir = 0;
        break;
    }

    int right_pwm = msg % 1000;
    int left_pwm = msg / 1000;
    Serial.print("\nLeft: ");
    Serial.print(left_pwm);
    Serial.print(" Right: ");
    Serial.print(right_pwm);


    // Command motors
    moveRight(right_pwm, right_dir);
    moveLeft(left_pwm, left_dir);
  }
}

