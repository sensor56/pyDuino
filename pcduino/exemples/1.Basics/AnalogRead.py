#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# test analogRead

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	
	#voie A0
	mesure=analogRead(A0) # mesure la voie A0
	tension = mesure*2000.0/63.0 # voie A0 et A1 = 6 bits (0-63) sur plage 0-2V 
	
	Serial.println (" Voie A0 = " + str(mesure) + " soit " + str("%.2f" % tension) + " mV." )
	
	#voie A2
	mesure=analogRead(A2) # mesure la voie A2
	tension = mesure*3300.0/4095.0 # voie A2 à A5 = 12 bits (0-4095) sur plage 0-3.3V 
	
	Serial.println (" Voie A2 = " + str(mesure) + " soit " + str("%.2f" % tension) + " mV." )
	
	#voie A2
	mesuremV=analogReadmV(A2) # mesure la voie A2 - résultat en mV
	Serial.println("Voie A2 = " + str(mesuremV) + " mV.")
	
	delay(1000)# entre 2 mesures 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin




