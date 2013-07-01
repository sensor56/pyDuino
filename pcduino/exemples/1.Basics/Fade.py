#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# La luminosite d'une LED varie (PWM) en fonction mesure analogique

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	
	#voie A2
	mesure=analogRead(A2) # mesure la voie A2
	tension=rescale(mesure,0,4095,0,3300.0) # voie A2 à A5 = 12 bits (0-4095) sur plage 0-3.3V 
	#tension = mesure*3300.0/4095.0 # calcul équivalent 
	
	Serial.println (" Voie A2 = " + str(mesure) + " soit " + str("%.2f" % tension) + " mV." )
	
	impuls=rescale(mesure,0,4095,0,255) # calcul largeur PWM par rescale 0-4095 vers 0-255
	analogWrite(PWM0, impuls) # applique la largeur fonction de la mesure analogique
	
	Serial.println("PWM=" + str(impuls)) # affiche largeur
	
	delay(200)# entre 2 mesures 
	
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




