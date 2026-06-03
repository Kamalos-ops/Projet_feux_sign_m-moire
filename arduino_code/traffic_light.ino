int lanes[4][3] = {
  {2,3,4},
  {5,6,7},
  {8,9,10},
  {11,12,13}
};

void setup() {
  Serial.begin(9600);
  for(int i=0;i<4;i++){
    for(int j=0;j<3;j++){
      pinMode(lanes[i][j], OUTPUT);
    }
  }
}

void activateLane(int lane){
  for(int i=0;i<4;i++){
    digitalWrite(lanes[i][0], HIGH);
    digitalWrite(lanes[i][1], LOW);
    digitalWrite(lanes[i][2], LOW);
  }
  digitalWrite(lanes[lane][0], LOW);
  digitalWrite(lanes[lane][2], HIGH);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    if (cmd.startsWith("LANE_")) {
      int lane = cmd.substring(5).toInt();
      activateLane(lane);
    }
  }
}
