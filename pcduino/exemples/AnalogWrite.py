#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# code test analogWrite

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True # pas de fonction loop = economise cpu 

#--- setup --- 
def setup():
  
	#setFrequencePWM(PWM1,195) # fixe fréquence PWM parmi [195,260,390,520,781]Hz possible pour PWM1 et PWM2
	#analogWrite(PWM1,25) # largeur impulsion en 0-255
	#analogWritePercent(PWM1,50) # largeur impulsion en 0-100%
	
	setFrequencyPWM(PWM0,1500) # fixe fréquence PWM parmi [126 à 2000]Hz pour PWM0, PWM3, PWM4, PWM5

	#analogWriteHardware(PWM0,237) # largeur impulsion matérielle
	# 15 pour 2000Hz et 240 pour 125Hz
	# en fait, ~ 33000/F... par deduction sur l'oscillo... 
	
	#analogWrite(PWM0,127) # largeur impulsion en 0-255
	analogWritePercent(PWM0,50) # largeur impulsion en 0-100%
	#analogWritePercent(PWM0,0) # largeur impulsion en 0-100% => 0% = stop PWM

	# duty natif entre 0 et 60 d'après tests oscillo en 520 pour 3/9/10/11 (PWM0, PWM3, PWM4,PWM5)
	# duty natif entre 0 et 255 5/6 (PWM1, PWM2)
	# duty analogWrite rescale en 0-255 pour toutes les voies
	# duty analogWritePercent rescale en 0-100 pour toutes les voies 
	
	# la fréquence Pyduino par défaut est fixée à 520 Hz dans Pyduino (Arduino utilise 490 Hz environ)
	# donc setFrequencePWM pas obligatoire
	# broches PWM 3/9/10/11 supporte frequences[125-2000]Hz à differents dutycycle
	# broches PWM 5/6 supporte frequences [195,260,390,520,781]Hz à 256 dutycycle
	
	

# -- fin setup -- 

# -- loop -- 
def loop():
	return # si vide 
# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




