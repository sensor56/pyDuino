#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

"""
 * Copyright (c) 2013-2014 by Xavier HINAULT - support@mon-club-elec.fr
 *
 * This file is free software; you can redistribute it and/or modify
 * it under the terms of either the GNU General Public License version 3
 * or the GNU Lesser General Public License version 3, both as
 * published by the Free Software Foundation.
"""

""""
Ce fichier est partie intégrante  du projet pyDuino.

pyDuino apporte une couche d'abstraction au langage Python 
afin de pouvoir utiliser les broches E/S de mini PC
avec des instructions identiques au langage Arduino

Ce fichier est la version pour Arduino + PC
"""

# modules utiles

from pyduinoCoreCommon import * # variables communes
#from pyduino_hardware_pcduino import *
from pyduinoCoreBase import *
#from pyduinoCoreSystem import *
#from pyduinoCoreLibs import *


# variables globales du module 


# ==================== Fonctions spécifiques pour une plateforme donnée =============================
# =====================>>>>>>>>>> version Arduino + PC <<<<<<<<<<< =======================================

# ---- gestion broches E/S numériques ---

# ---- gestion broches E/S numériques ---

# pinMode 
def pinMode(pin, mode):
	
	
	
	if mode==OUTPUT : 
		common.Uart.println("pinMode("+str(pin)+",1)") # envoi commande - attention OUTPUT c'est 1
		
		out=None
		while not out : # attend reponse 
			out=common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode==INPUT : 
		out=None
		while not out : # tant que pas de reponse envoie une requete
			common.Uart.println("pinMode("+str(pin)+",0)") # attention input c'est 0
			#print ("pinMode("+str(pin)+",0)") # debug 
			
			out=common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode==PULLUP : 
		common.Uart.println("pinMode("+str(pin)+",0)") # attention INPUT c'est 0
		delay(100) # laisse temps reponse arriver
		print "pinMode("+str(pin)+",0)"
		
		out=None
		while not out : # attend reponse
			out=common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
		digitalWrite(pin,HIGH) # activation du pullup 
	
# digitalWrite 
def digitalWrite(pin, state):
	
	
	common.Uart.println("digitalWrite("+str(pin)+","+str(state)+")") # 
	#print ("digitalWrite("+str(pin)+","+str(state)+")") # debug

# digitalRead
def digitalRead(pin):
	
	
	# envoi de la commande
	common.Uart.println("digitalRead("+str(pin)+")") 
	print ("digitalRead("+str(pin)+")")
	# attend un reponse
	out=None
	while not out : # tant que pas de reponse envoie une requete
		out=common.Uart.waiting() # lit les caracteres
	
	print out # debug
	#out=out.splitlines()
	
	return out # renvoie la valeur



def toggle(pin): # inverse l'etat de la broche
	
	
	
	if digitalRead(pin)==HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

def pulseOut(pin, duree): # crée une impulsion sur la broche de durée voulue
	# pin : broche
	# duree : duree du niveau INVERSE en ms
	
	if digitalRead(pin)==HIGH: # si broche au niveau HAUT
		digitalWrite(pin,LOW) # mise au niveau BAS
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,HIGH) # mise au niveau HAUT
	else: # si broche au niveau BAS
		digitalWrite(pin,HIGH) # mise au niveau HAUT
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,LOW) # mise au niveau bas
	
	# cette fonction ne prétend pas à la précision à la µs près... 
	# mais a pour but d'éviter la saisie des 3 instructions en la remplaçant par une seule

#----- gestion broches analogique -----

# analogRead - entrées analogiques 
def analogRead(pinAnalog):
	
	
	""" 
	# mis en fin de lib' = exécution obligatoire au démarrage 
	# au besoin : initialisation port série 
	#global uartPort
	#if not uartPort : 
	#	Uart.begin(115200)
	#	Uart.waitOK() # attend port serie OK 
	"""
	# envoi la commande
	common.Uart.println("analogRead("+str(pinAnalog)+")") # 
	
	# attend une réponse 
	out=None
	while not out : # tant que pas de reponse 
		#print ("analogRead("+str(pinAnalog)+")") # debug
		#delay(50) # attend reponse
		out=common.Uart.waiting() # lit les caracteres
	
	if debug: print out # debug
	
	outlines=out.splitlines() # extrait les lignes... une manière simple de supprimer le fin de ligne
	if outlines[0].isdigit() :
		return int(outlines[0]) # renvoie la valeur
	else:
		return(-1)	

#----- analogRead avec repetition des mesures ---- 
def analogReadRepeat(pinAnalogIn,repeatIn):
	
	sommeMesures=0
	
	# réalise n mesures 
	for i in range(repeatIn): 
		sommeMesures=sommeMesures+analogRead(pinAnalogIn)
		# print i # debug 
		
	moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 
	
	return moyenne
	

# analogReadmV - entrées analogiques - renvoie valeur en millivolts
def analogReadmV(*args):
	
	# 2 formes :
	#pinAnalog
	#pinAnalog, rangeIn, mVIn où range est la resolution et mV la tension max = qui renvoie 4095
	# la 2ème forme permet utiliser étalonnage réel de la mesure
	
	# A0 et A1 : résolution 6 bits (0-63) en 0-2V
	# A2, A3, A4, A5 : résolution 12 bits (0-4095) en 0-3.3V
	
	# gestion paramètres 
	if len(args)==1: # forme pinAnalog
		pinAnalog=args[0]
	
		mesure=analogRead(pinAnalog)
		
		if pinAnalog==A0 or pinAnalog==A1:
			mesure=rescale(mesure,0,63,0,2000)
		elif pinAnalog==A2 or pinAnalog==A3 or pinAnalog==A4 or pinAnalog==A5:
			#mesure=rescale(mesure,0,4095,0,3300)
			mesure=rescale(mesure,0,4095,0,3000) # en pratique, la mesure 4095 est atteinte à 3V.. 
			
	else: # forme pinAnalog, range, mV où range est la resolution et mV la tension max = qui renvoie 4095
		pinAnalog=args[0]
		rangeIn=args[1] 
		mVIn=args[2]
		
		mesure=analogRead(pinAnalog) # mesure sur la broche 
		
		mesure=rescale(mesure,0,rangeIn,0,mVIn) # en pratique, la mesure 4095 est atteinte à 3V.. 
		
	return mesure

#----- analogRead avec repetition des mesures ---- 
def analogReadmVRepeat(*args):
	
	# formes :
	# pinAnalogIn,repeatIn
	# pinAnalogIn,repeatIn, rangeIn, mVIn
	
	sommeMesures=0
	
	if len(args)==2: # si forme pinAnalogIn,repeatIn
		pinAnalogIn=args[0]
		repeatIn=args[1]

		# réalise n mesures avec la forme analogReadmV(pinAnalogIn) 
		for i in range(repeatIn): 
			sommeMesures=sommeMesures+analogReadmV(pinAnalogIn)
			# print i # debug 
			
		moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 
		
	else: 	# pinAnalogIn,repeatIn, rangeIn, mVIn
		pinAnalogIn=args[0]
		repeatIn=args[1]
		rangeIn=args[2]
		mVIn=args[3]
		
		# réalise n mesures avec la forme analogReadmV(pinAnalogIn, rangeIn, mVIn) 
		for i in range(repeatIn): 
			sommeMesures=sommeMesures+analogReadmV(pinAnalogIn, rangeIn, mVIn)
			# print i # debug 
			
		moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 

	return moyenne
	

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	Uart.println("analogWrite("+str(pinPWMIn)+","+str(largeurIn)+")") # 
	print ("analogWrite("+str(pinPWMIn)+","+str(largeurIn)+")") # debug 

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	global uartPort
	
	if not uartPort : 
		Uart.begin(115200)

	analogWrite(pinPWMIn,rescale(largeurIn,0,100,0,255))
	

# tone
def tone(pinPWMIn,frequencyIn):
	setFrequencyPWM(pinPWMIn, frequencyIn) # modifie la fréquence - attention aux valeurs limites possibles
	analogWrite(pinPWMIn,127) # onde 50% largeur 
	

# noTone
def noTone(pinPWMIn):
	setFrequencyPWM(pinPWMIn, 520) # restaure fréquence par défaut - et impulsion mise à 0%
	analogWrite(pinPWMIn,0) # onde 0% largeur # pas indispensable normalement 
	
