pyDuino
=======

## Intro

pyDuino apporte une couche d'abstraction au langage Python afin de pouvoir utiliser les broches E/S de mini-PC tels que RaspberryPi ou le pcDuino avec des instructions identiques au langage Arduino. 

## Versions disponibles

La librairie existe en plusieurs versions : 
* sur le pcDuino : 
** en version standard
** en version multimédia

* sur le RaspberryPi : 
** en version standard


## Installation 

* sur le pcDuino, dans un Terminal, saisir la commande : 

	sudo wget -4 -N https://raw.github.com/sensor56/pyDuino/master/pcduino/pyduino.py /usr/lib/python2.7/dist-packages
	
* sur le raspberryPi, dans un Terminal, saisir la commande :

	sudo wget -4 -N https://raw.github.com/sensor56/pyDuino/master/RaspberryPi/pyduino.py /usr/lib/python2.7/dist-packages
	

## Documentation officielle 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.HomePage

## Fonctions Arduino implémentées 

* pinMode(broche, mode)
* digitalWrite(broche, valeur)
* digitalRead(broche) --> int
* toggle(broche) 

* analogRead(brocheAnalog) --> int
* analogReadmV(brocheAnalog) --> float 

* analogWrite(brochePWM, valeur) - PWM 0-255
* analogWritePercent(brochePWM, valeur) - PWM 0-100%
* analogWriteHardware(brochePWM, valeur) - PWM
* setFrequencyPWM(broche, frequence) 

* millis() --> int
* micros() --> int
* delay(ms)
* delayMicroseconds(us)
* year() -->int
* month() -->int
* day() -->int
* hour() -->int
* minutes() -->int
* seconds() -->int
* unixtime() -->int 

## Utilisation 

L'utilisation se veut la plus simple possible : un seul fichier à installer dans le répertoire du/des scripts Python.


L'utilisation ensuite est simple : importation du module sous la forme : 
	
	from pyduino import * # importe les fonctions Arduino pour Python 
	
En fin de code, on ajoute les lignes suivantes pour rendre le script exécutable : 

	if __name__=="__main__": # pour rendre le code executable 
  		setup() # appelle la fonction main
		while(1): loop() # appelle fonction loop sans fin
	
	
Une fois fait, on accède au sein du code Python aux fonctions Arduino comme on le ferait dans un code Arduino natif. 

## Exemple : 

	#!/usr/bin/python
	# -*- coding: utf-8 -*-

	from arduino import * # importe les fonctions Arduino pour Python

	# entete declarative
	LED=2   # broche utilisée pour la LED
	
	#--- setup --- 
	def setup():
 	 
		pinMode(LED,OUTPUT) # met la broche en sortie

	# -- loop -- 
	def loop():
	
		digitalWrite(LED, HIGH) # allume la LED
		Serial.println('LED allumée')
		delay(1000)  # pause en millisecondes
		
		digitalWrite(LED,LOW) # eteint LED
		Serial.println('LED éteinte')
		delay(1000) # pause en millisecondes

	# fin loop
	
	#--- obligatoire pour lancement du code -- 
	if __name__=="__main__": # pour rendre le code executable 
		setup() # appelle la fonction main
		while(1): loop() # appelle fonction loop sans fin

