//--- Arduino live avec la librairie Utils ---
// Par X. HINAULT - Juin 2013
// Tous droits réservés - GPLv3

#include <Utils.h> // inclusion de la librairie
// A télécharger ici : https://github.com/sensor56/Utils/archive/master.zip 

Utils utils; // déclare objet racine d'accès aux fonctions de la librairie Utils

String chaineReception=""; // déclare un String
long params[6]; // déclare un tableau de long - taille en fonction nombre max paramètres attendus

int pin=255;
int state=255; 
int pwm=0;
int mode=255; 

void setup() {

  Serial.begin(115200); // Initialisation vitesse port Série
  // Utiliser vitesse idem coté Terminal série
  
  Serial.println("Arduino OK!"); // message debut Arduino OK - nécessaire pour initialisation Pyduino

} // fin setup

void loop() {

    //chaineReception=utils.waitingString(true);// avec debug
    chaineReception=utils.waitingString();// sans debug

    if (chaineReception!="") { // si une chaine a été reçue

      //--- pinMode() --- 
      if(utils.testInstructionLong(chaineReception,"pinMode(",2,params)==true) { // si chaine voulue bien recue
  
            //Serial.println("Arduino a recu le parametre : " + (String)params[0]); // debug
            //Serial.println("Arduino a recu le parametre : " + (String)params[1]); // debug
            
            pin=params[0]; 
            mode=params[1];
            
            pinMode(pin,mode); // attention mode 1 = output et mode 0 = Input... 

            Serial.println(">"); // renvoi saut de ligne de validation
              
      } // fin si testInstructionLong==true


      //--- digitalWrite() --- 
      if(utils.testInstructionLong(chaineReception,"digitalWrite(",2,params)==true) { // si chaine voulue bien recue
  
            //Serial.println("Arduino a recu le parametre : " + (String)params[0]); // debug
            //Serial.println("Arduino a recu le parametre : " + (String)params[1]); // debug
            
            pin=params[0]; 
            state=params[1];
            
            digitalWrite(pin,state);

            Serial.println(); // renvoi saut de ligne de validation
            
              
      } // fin si testInstructionLong==true

      //--- digitalRead() --- 
      //if(utils.testInstructionLong(chaineReception,"analogRead(",1,params, true)==true) { // si chaine voulue bien recue - avec debug
      if(utils.testInstructionLong(chaineReception,"digitalRead(",1,params)==true) { // si chaine digitalRead( bien recue
  
            //Serial.println("Arduino a recu le parametre : " + (String)params[0]); // debug
  
            pin=params[0]; 
            
            state=digitalRead(pin); // appelle fonction voulue
            
            //Serial.print("[");
            //Serial.print(state); // envoi valeur sous la forme [ .. ]
            //Serial.println("]");

            Serial.println(state); // envoi valeur sous la forme .. 
            
  
      } // fin si testInstructionLong==true

      //--- analogRead() --- 
      //if(utils.testInstructionLong(chaineReception,"analogRead(",1,params, true)==true) { // si chaine voulue bien recue - avec debug
      if(utils.testInstructionLong(chaineReception,"analogRead(",1,params)==true) { // si chaine analogRead( bien recue
  
            //Serial.println("Arduino a recu le parametre : " + (String)params[0]); // debug
  
            pin=params[0]; 
            
            int mesure=analogRead(pin); // appelle fonction voulue
            
            //Serial.print("[");
            //Serial.print(mesure); // envoi valeur sous la forme [ .. ]
            //Serial.println("]");
            Serial.println(mesure); // envoi valeur sous la forme .. 
  
      } // fin si testInstructionLong==true

      //--- analogWrite() --- 
      if(utils.testInstructionLong(chaineReception,"analogWrite(",2,params)==true) { // si chaine voulue bien recue
  
            //Serial.println("Arduino a recu le parametre : " + (String)params[0]); // debug
            //Serial.println("Arduino a recu le parametre : " + (String)params[1]); // debug
            
            pin=params[0]; 
            pwm=params[1];
            
            analogWrite(pin,pwm);
            
            Serial.println(); // renvoi saut de ligne de validation

              
      } // fin si testInstructionLong==true
      
      

    } // fin // si une chaine a été reçue

} // fin loop
