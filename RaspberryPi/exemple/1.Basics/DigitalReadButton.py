#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test digitalRead avec bouton poussoir

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
BP=0  # declare la broche a utiliser
APPUI=LOW # valeur broche lors appui

#--- setup --- 
def setup():
  pinMode(BP,PULLUP) # met la broche en entree avec rappel au plus actif
	Serial.println("La broche 0 est en entrée avec rappel au plus actif !")

# -- fin setup -- 

# -- loop -- 
def loop():
	
	if(digitalRead(BP)==APPUI): # si appui
		Serial.println("Appui BP!")
		delay(250)  # anti-rebond
	
	delay(100) # pause entre 2 lecture du BP
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin
