int EN_A = 3; 
int PinIN1 = 5;
int PinIN2 = 4;  
int EN_B = 6; 
int PinIN3 = 9;
int PinIN4 = 8; 

void setup()
{
Serial.begin(9600);
pinMode(EN_A, OUTPUT);
pinMode(PinIN1, OUTPUT); 
pinMode(PinIN2, OUTPUT);
pinMode(PinIN3, OUTPUT); 
pinMode(PinIN4, OUTPUT); 
pinMode(EN_B, OUTPUT); 

} 
 
void loop()  
{

if (Serial.available()){
  char c=Serial.read();
  if(c=='W'){
    Adelante();
    //delay(180);
  }
  else if(c=='S'){
    Atras();
    //delay(180);
  }
  else if(c=='E'){
    AdelanteD();
    //delay(180);
  }
  else if(c=='Q'){
    AdelanteI();
    //delay(180);
  }
  else if(c=='C'){
    AtrasD();
    //delay(180);
  }
    else if(c=='D'){
    Derecha();
    //delay(180);
  }
  else if(c=='A'){
    Izquierda();
    //delay(180);
  }
  else if(c=='Z'){
    AtrasI();
    //delay(180);
  }
  else if(c=='X'){
    Parada();
    //delay(180);
  }
    else if(c=='P'){
    Stop();
    //delay(180);
  }
  
  } 
  
}
void Adelante()
{
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN2, LOW);
  analogWrite(EN_A, 100);
}
void Atras()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, HIGH);
  analogWrite(EN_A, 100);
}
void AdelanteD()
{
  digitalWrite (PinIN3, HIGH);
  digitalWrite (PinIN4, LOW);
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN2, LOW);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void AdelanteI()
{
  digitalWrite (PinIN3, LOW);
  digitalWrite (PinIN4, HIGH);
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN2, LOW);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void AtrasD()
{
  digitalWrite (PinIN3, HIGH);
  digitalWrite (PinIN4, LOW);
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, HIGH);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void AtrasI()
{
  digitalWrite (PinIN3, LOW);
  digitalWrite (PinIN4, HIGH);
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, HIGH);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void Stop()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, LOW);
  digitalWrite (PinIN3, LOW);
  digitalWrite (PinIN4, LOW);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void Parada()
{
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN2, HIGH);
  digitalWrite (PinIN3, HIGH);
  digitalWrite (PinIN4, HIGH);
  analogWrite(EN_A, 100);
  analogWrite(EN_B, 255);
}
void Derecha()
{
  digitalWrite (PinIN3, HIGH);
  digitalWrite (PinIN4, LOW);
  analogWrite(EN_B, 255);
}
void Izquierda()
{

  digitalWrite (PinIN3, LOW);
  digitalWrite (PinIN4, HIGH);
  analogWrite(EN_B, 255);
}
