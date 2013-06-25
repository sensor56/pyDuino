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

HIGH = 1
LOW =  0

A0, A1, A2, A3, A4,A5 =0,1,2,3,4,5 # identifiant broches analogiques

# --- fonctions Arduino ---- 

# pinMode 
def pinMode(pin, mode):
	
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# fixe le mode de la broche E/S
	file=open(pathMode+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(mode) # ecrit dans le fichier le mode voulu
	file.close()

# digitalWrite 
def digitalWrite(pin, state):
	
	pin=int(pin)
	state=str(state) # transforme en chaine
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(state)
	file.close()
	

# digitalRead
def digitalRead(pin):
	
	pin=int(pin)
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'r') # ouvre le fichier en lecture
	file.seek(0) # se place au debut du fichier
	state=file.read()  #lit le fichier
	#print state #debug
	file.close()
	
	return int(state)  # renvoie valeur entiere
	

# analogRead
def analogRead(pin):
	
	pin=int(pin) # pin est un int entre 0 et 5 - utilisation identifiant predefini possible
	
	# lecture du fichier
	file=open('/proc/adc'+str(pin),'r')
	file.seek(0)  # en debut du fichier
	out=file.read() # lit la valeur = un str de la forme adc 0 : valeur
	file.close()
	
	# extraction de la valeur
	out=out.split(":") # scinde la chaine en 2
	out=out[1] # garde la 2eme partie = la valeur
	
	return int(out) # renvoie la valeur

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
