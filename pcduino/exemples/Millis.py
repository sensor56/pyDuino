#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test millis()

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
millis0=0 # variable pour mémoriser millis()
delai=1000 # delai d'attente

#--- setup --- 
def setup():
  
	global millis0   # millis0 est une variable globale
	
	Serial.begin(115200) # émulation Serial.begin - pas indispensable
	
	millis0=millis()  # mémorise millis()
	
# -- fin setup -- 

# -- loop -- 
def loop():
	
	global millis0 # millis0 est une variable globale
	
	if millis()-millis0>delai : # si le délai est écoulé
		Serial.println(str(millis()) + "ms ecoulees depuis le lancement du code") # affiche message
		millis0=millis()  # mémorise nouveau millis()
	

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
