pyDuino
=======

## Intro

pyDuino apporte une couche d'abstraction au langage Python afin de pouvoir utiliser les broches E/S de mini-PC tels que RaspberryPi ou le pcDuino avec des instructions identiques au langage Arduino. 

## Fonctions Arduino implémentées 

* pinMode()
* digitalWrite()
* digitalRead()

* analogRead()

* millis()
* delay()

* Serial.println() (Emulation affichage Série dans la console système) 

## Utilisation 

L'utilisation se veut la plus simple possible : un seul fichier à installer dans le répertoire du/des scripts Python. Un module système sera disponible prochainement. 

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

