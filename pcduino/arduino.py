#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

""""
Ce fichier est partie intégrante  du projet pyDuino.

pyDuino apporte une couche d'abstraction au langage Python 
afin de pouvoir utiliser les broches E/S de mini PC
avec des instructions identiques au langage Arduino

L'utilisation se veut la plus simple possible :
un seul fichier à installer. 

Ce fichier est la version pour le pcDuino
"""
# modules utiles 
import time

# -- declarations --

# sur le pcDuino, la plupart des operations passent par des fichiers systeme

# fichiers broches E/S pcDuino
pathMode="/sys/devices/virtual/misc/gpio/mode/"
pathState="/sys/devices/virtual/misc/gpio/pin/"

# constantes Arduino like
INPUT="0"
OUTPUT="1"
PULLUP="8"

HIGH = "1"
LOW =  "0"


# --- fonctions Arduino ---- 

# pinMode 
def pinMode(pin, mode):
  
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# fixe le mode de la broche E/S
	file=open(pathMode+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(OUTPUT)
	file.close()

# digitalWrite 
def digitalWrite(pin, state):
	
	pin=int(pin)
	state=str(state)
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'w') # ouvre le fichier en lecture
	file.write(state)
	file.close()

# delay
def delay(ms):
	
	int(ms)
	
	time.sleep(ms/1000.0) # pause en secondes



# classe Serial pour émulation affichage message en console
class Serial():
	
	# def __init__(self): # constructeur principal
	
	def println(self,text):
		
		#text=str(txt)
		
		print(text)
		


# fin classe Serial 
  
Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
