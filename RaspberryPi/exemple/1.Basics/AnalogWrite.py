#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple Pyduino - par X. HINAULT - www.mon-club-elec.fr
# voir : https://github.com/sensor56/pyDuino

# test analogWrite - impulsion PWM 

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True # n'execute pas la fonction loop = decharge CPU

#--- setup --- 
def setup():
  #analogWrite(PWM0,200)
	analogWritePercent(PWM0,10) # pwm avec largeur exprime en %
	
	# frequence utilisee = 5000 Hz
	# duty natif = 0-1023 rescaler en 0-255 par la fonction analogWrite
	# une seule broche PWM0 = I/O 1 peut etre utilisee en PWM sur le raspberryPi
	# analogWritePercent recoit valeur en % (0-100) 
	
	
# -- fin setup -- 

# -- loop -- 
def loop():
	return # si vide 

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin
