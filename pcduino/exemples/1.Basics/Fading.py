#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# La luminosite d'une LED varie (PWM) 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
LED=PWM0 # broche pour la LED - doit être une broche PWM (3,5,6,9,10 ou 11)

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	
	for impuls in range(0,255):
		analogWrite(PWM0, impuls) # applique la largeur 
		Serial.println ("PWM= "+str(impuls))
		delay(10)# entre 2 changements
	
	for impuls in range(0,255):
		analogWrite(PWM0, 255-impuls) # applique la largeur 
		Serial.println ("PWM= "+str(255-impuls))
		delay(10)# entre 2 changements
		
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




