#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test micros()

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
micros0=0 # variable pour mémoriser micros()
delai=1000000 # delai d'attente

#--- setup --- 
def setup():
  
	global micros0   # micros0 est une variable globale
	
	Serial.begin(115200) # émulation Serial.begin - pas indispensable
	
	micros0=micros()  # mémorise micros()
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global micros0 # millis0 est une variable globale
	
	if micros()-micros0>delai : # si le délai est écoulé
		Serial.println(str(micros()) + "us ecoulees depuis le lancement du code") # affiche message
		micros0=micros()  # mémorise nouveau micros()
	

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




