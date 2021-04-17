//Declare pin functions on Arduino
#include <TimerOne.h>
#include <Stepper.h>

//Motor
int stepsPerRevolution=2048;
float motSpeed = 0;
int dt=500;
int motDir=1;
Stepper myStepper(stepsPerRevolution, 4,6,5,7);


//User
String user_input;
String usr_in;
float x;
int state;
void StepForwardDefault();
void ReverseStepDefault();
float rot;
String dat0;
String dat1;
int flag = 0;

void setup() {
  // Motor
  Serial.begin(9600);
  myStepper.setSpeed(motSpeed);
  Timer1.initialize(1000);
  Timer1.attachInterrupt(toggle);
  flag = 0;
}
 
void loop() 
{
  flag = 0;
  if(flag == 0){
    while(Serial.available() > 0)
    {
      user_input = Serial.readStringUntil('\n');
      if (user_input == "F")     
        {
          StepForwardDefault();  
          flag = 1;
        }
        else if(user_input =="B") 
        {
          ReverseStepDefault();     
        }
     }
  }
  else if(flag == 1){
      
  }
}



//Default microstep mode function
void StepForwardDefault()
{   
  dat0 = Serial.readStringUntil(',');
  motSpeed = dat0.toFloat();
  dat1 = Serial.readStringUntil('\n');
  rot = dat1.toFloat();
  Serial.flush();
  myStepper.setSpeed(motSpeed);
  for(x= 1; x<rot; x++)  //Loop the forward stepping enough times for motion to be visible 
  { 
    myStepper.step(2048);
    if(flag == 1){
      break;
    }
   }
   Serial.print("Finished\n");
 } 
 
//Reverse default microstep mode function
void ReverseStepDefault()
{ 
  Serial.flush();
  motSpeed = 8;
  myStepper.setSpeed(motSpeed);
  Serial.println("Moving in reverse at default step mode.");
  for(x= 1; x<8; x++)  //Loop the stepping enough times for motion to be visible  
    { 
      myStepper.step(2048*(-1));  
    }   
 } 
 

//The following function is meant to pause and resume the function
//it is an interrupt which means it will always be running while the main code is
//it will be called when the corresponding pause or resume buttons are pressed
//may turn into just a hard stop button
 void toggle(){
  while(Serial.available() > 0){
    usr_in = Serial.readStringUntil('\n');
      if(usr_in == "P"){
        if(flag == 0){
          flag = 1;
        }
        else if(flag = 1){
        flag = 0;
        }
      }
  }
 }
