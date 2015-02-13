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

Ce fichier est la version pour le pcDuino
"""
# message d'accueil 
print("Pyduino for pcDuino - by www.mon-club-elec.fr - 2015 ")

# modules utiles 

"""
#-- temps --
import time
import datetime # gestion date 

from threading import Timer # importe l'objet Timer du module threading

#-- math -- 
# import math
from math import *  # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()
"""

""" Pyduino hardware
#-- pour PWM - accès kernel + transposition C to Python -- 
import fcntl # module pour fonction ioctl
#from ctypes import *
import ctypes # module pour types C en Python 
"""

"""
#-- système -- 
import subprocess
#import getpass # pour connaitre utilisateur systeme 
import os  # gestion des chemins
import glob # listing de fichiers
"""

#--- expressions regulieres
import re # expression regulieres pour analyse de chaines

# serie Uart
try:
	import serial
except: 
	print("ATTENTION : Module Serial manquant : installer le paquet python-serial ")

"""
# reseau 
import socket 
import smtplib # serveur mail 
"""

#--- module des variables communes partagées entre les éléments Pyduino -- 
import pyduinoCoreCommon as common

# -- declarations --
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop ou de passer par un fichier commun... 

# sur le pcDuino, la plupart des operations passent par des fichiers systeme
# important : pour réaffecter la valeur d'une variable partagée = IL FAUT UTILISER LE NOM DU MODULE - sinon variable globale module, pas partagée... 

common.PLATFORM="PCDUINO"

# fichiers broches E/S pcDuino
common.pathMode="/sys/devices/virtual/misc/gpio/mode/"
common.pathState="/sys/devices/virtual/misc/gpio/pin/"

# constantes Arduino like spécifique de la plateforme utilisée 
common.INPUT="0"
common.OUTPUT="1"
common.PULLUP="8"

common.A0, common.A1, common.A2, common.A3, common.A4,common.A5 =0,1,2,3,4,5 # identifiant broches analogiques
common.PWM=[3,5,6,9,10,11] # list pour acces par indice
common.PWM0, common.PWM1, common.PWM2, common.PWM3, common.PWM4,common.PWM5 =common.PWM[0],common.PWM[1],common.PWM[2],common.PWM[3],common.PWM[4],common.PWM[5] # identifiant broches PWM

#-- les sous modules Pyduino utilisés par ce module - à mettre après les variables spécifiques ci-dessus --
from pyduinoCoreBase import *
from pyduino_hardware_pcduino import *
from pyduinoCoreSystem import *
from pyduinoCoreLibs import *

######################## Fonctions Libs dédiées ################################

# et classes implémentées localement

# classe Uart pour communication série UART 
class Uart():
	
	# def __init__(self): # constructeur principal
	
	
	def begin(self,rateIn, *arg): # fonction initialisation port serie 
		
		
		# arg = rien ou timeout ou timeout et port a utiliser
		global uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		pinMode(RX,UART)
		pinMode(TX,UART)
		
		#-- initialisation port serie uart 
		try:
			if len(arg)==0: # si pas d'arguments
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
				uartPort=serial.Serial('/dev/ttyS1', rateIn, timeout = 10) # initialisation port serie uart
				print("Initialisation Port Serie : /dev/ttyS1 @ " + str(rateIn) +" = OK ") # affiche debug
			elif len(arg)==1 : # si timeout
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort=serial.Serial('/dev/ttyS1', rateIn, timeout = arg[0]) # initialisation port serie uart
				print("Initialisation Port Serie : /dev/ttyS1 @ " + str(rateIn) +" = OK ") # affiche debug
				print("timeout = " + str(arg[0] ))
			elif len(arg)==2 : # si timeout et port 
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort=serial.Serial(arg[1], rateIn, timeout = arg[0]) # initialisation port serie uart
				print("Initialisation Port Serie : "+ arg[1] + " @ " + str(rateIn) +" = OK ") # affiche debug
				print("timeout = " + str(arg[0] ))
		except:
			print("Erreur lors initialisation port Serie") 
			
	def println(self,text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text=str(text) # au cas où
		# print "text =" + text # debug
		
		arg=list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg)==0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0]==DEC and text.isdigit():
				out=text
				#print(out) # debug
			elif arg[0]==BIN and text.isdigit():
				out=bin(int(text))
				#print(out) # debug
			elif arg[0]==OCT and text.isdigit():
				out=oct(int(text))
				#print(out) # debug
			elif arg[0]==HEX and text.isdigit():
				out=hex(int(text))
				#print(out) # debug
		else: # si pas de formatage de chaine = affiche tel que 
			out=text
			#print(out) # debug
		
		uartPort.write(out+chr(10)) # + saut de ligne 
		# print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		uartPort.flush()
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	
	"""
	# idem println mais sans le saut de ligne... 
	def print(self,text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text=str(text) # au cas où
		# print "text =" + text # debug
		
		arg=list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg)==0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0]==DEC and text.isdigit():
				out=text
				#print(out) # debug
			elif arg[0]==BIN and text.isdigit():
				out=bin(int(text))
				#print(out) # debug
			elif arg[0]==OCT and text.isdigit():
				out=oct(int(text))
				#print(out) # debug
			elif arg[0]==HEX and text.isdigit():
				out=hex(int(text))
				#print(out) # debug
		else: # si pas de formatage de chaine = affiche tel que 
			out=text
			#print(out) # debug
		
		uartPort.write(out) # sans saut de ligne
		# print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	"""
	
	def available(self):
		global uartPort
		
		if uartPort.inWaiting() : return True
		else: return False
		
	def flush(self):
		global uartPort
		return uartPort.flush()
	
	def read(self):
		global uartPort
		return uartPort.read()
	
	def write(self, strIn):
		global uartPort
		uartPort.write(strIn)
		
	
	
	#--- lecture d'une ligne jusqu'a caractere de fin indique
	def waiting(self, *arg): # lecture d'une chaine en reception sur port serie 
		
		global uartPort
		
		if len(arg)==0: endLine="\n" # par defaut, saut de ligne
		elif len(arg)==1: endLine=arg[0] # sinon utilise caractere voulu
		
		#-- variables de reception -- 
		chaineIn=""
		charIn=""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn=uartPort.read() # on lit le caractere
			#print charIn # debug
			
			if charIn==endLine: # si caractere fin ligne , on sort du while
				#print("caractere fin de ligne recu") # debug
				break # sort du while
			else: #tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn=chaineIn+charIn
				# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine
	
	#--- lecture de tout ce qui arrive en réception 
	def waitingAll(self): # lecture de tout en reception sur port serie 
		
		global uartPort
		
		#-- variables de reception -- 
		chaineIn=""
		charIn=""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn=uartPort.read() # on lit le caractere
			#print charIn # debug
			chaineIn=chaineIn+charIn
			# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine

# ajouter write / read   / flush 

# fin classe Uart


########################### --------- initialisation ------------ #################

common.Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Serial=common.Serial

common.Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Ethernet = common.Ethernet # declare instance Ethernet implicite pour acces aux fonctions 

common.Uart = Uart() # declare instance Uart implicite 
Uart=common.Uart

common.micros0Syst=microsSyst() # mémorise microsSyst au démarrage
common.millis0Syst=millisSyst() # mémorise millisSyst au démarrage


