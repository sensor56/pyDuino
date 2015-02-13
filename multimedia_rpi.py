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


"""
// ------- Licence du code de ce programme -----
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License,
//  or any later version.
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.

Voir : http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.Licence

"""

"""
Ce fichier est partie intégrante  du projet pyDuino.
Site officiel : http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.HomePage

pyDuino apporte une couche d'abstraction au langage Python 
afin de pouvoir utiliser les broches E/S de mini PC
avec des instructions identiques au langage Arduino

L'utilisation se veut la plus simple possible :
un seul fichier à installer. 

Ce fichier est la version pour le raspberryPi version B

"""
# message d'accueil
print "Pyduino Multimedia for Raspberry Pi - v0.4 - by www.mon-club-elec.fr - 2013 "

# modules utiles

"""
#-- temps --
import time
import datetime # gestion date

from threading import Timer # importe l'objet Timer du module threading

#-- math --
# import math
from math import * # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()
"""
#-- pour PWM - accès kernel + transposition C to Python --
import fcntl # module pour fonction ioctl
#from ctypes import *
import ctypes # module pour types C en Python

"""
#-- système --
import subprocess
#import getpass # pour connaitre utilisateur systeme
import os # gestion des chemins
import glob # listing de fichiers
"""

#--- expressions regulieres
import re # expression regulieres pour analyse de chaines

# serie
try:
	import serial
except:
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

"""
# reseau
import socket 
import smtplib # serveur mail 
"""

#-- les sous modules Pyduino utilisés par ce module --
from pyduinoCoreCommon import * # variables communes
from pyduinoCoreBase import *
from pyduinoCoreSystem import *
from pyduinoCoreLibs import *

from pyduinoCoreMultimedia import *

# on presuppose ici que wiringPi est present sur le systeme: 
# sudo apt-get install git 
# git clone git://git.drogon.net/wiringPi
# cd wiringPi
# git pull origin
# ./build

# doc de gpio ici : http://wiringpi.com/the-gpio-utility/

# -- declarations --

# sur le raspberryPi, la plupart des operations sont accessible avec la commande gpio 

# fichiers broches E/S raspberryPi
pathMain="/sys/class/gpio/gpio"
pinList=['17', '18', '27', '22', '23', '24', '25', '4'] # definition des borches I/O - version B
#pin=['17', '18', '21', '22', '23', '24', '25', '4'] # definition des borches I/O - version A

# constantes Arduino like
INPUT="in"
OUTPUT="out"
PULLUP="up" # accepte par commande gpio

A0, A1, A2, A3, A4,A5 =0,1,2,3,4,5 # identifiant broches analogiques
PWM0=1 # identifiant broches PWM

"""
HIGH = 1
LOW =  0

DEC=10
BIN=2
HEX=16
OCT=8

# pour uart
UART="3"
RX=0
TX=1

uartPort=None


# constantes Pyduino
noLoop=False 
debug=False # pour message debug

READ="r"
WRITE="w"
APPEND="a"
"""
"""
#--- chemin de reference ---
#user_name=getpass.getuser()
home_dir=os.getenv("HOME")+"/" # chemin de référence
main_dir=os.getenv("HOME")+"/" # chemin de référence

# constantes de SELECTION
TEXT='TEXT'
IMAGE='IMAGE'
AUDIO='AUDIO'
VIDEO='VIDEO'

#---- chemins data fichiers texte, sons, image, video

data_dir_text="data/text/" # data texte relatif a main dir
data_dir_audio="data/audio/" # data audio
data_dir_image="data/images/" # data images
data_dir_video="data/videos/" # data video

#---- chemins sources fichiers texte, sons, images, video
src_dir_text="sources/text/" # sources texte relatif a main dir
src_dir_audio="sources/audio/" # sources audio
src_dir_image="sources/images/" # sources images
src_dir_video="sources/videos/" # sources video
"""

# --- fonctions Arduino ---- 

#====================== fonctions specifiques de la plateforme ===================
#========================= fonctions RaspberryPi =================================

# pinMode 
def pinMode(pin, mode):
	
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	if mode==INPUT or mode==OUTPUT : # si in ou out 
		# en acces direct = plus rapide 
		file=open(pathMain+pinList[pin]+"/direction",'w') # ouvre le fichier en écriture
		file.write(OUTPUT)
		file.close()
	elif mode==PULLUP : # sinon = si up
		# fixe le mode de la broche E/S via ligne commande gpio 
		cmd="gpio mode "+str(pin)+" "+mode
		subprocess.Popen(cmd, shell=True)
		print cmd # debug
	

# digitalWrite 
def digitalWrite(pin, state):
	
	pin=int(pin)
	state=str(state) # transforme en chaine
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	# met la broche dans etat voulu via ligne de commande gpio
	#cmd="gpio write "+str(pin)+" "+str(state)
	#subprocess.Popen(cmd, shell=True)	
	#print cmd # debug
	
	# en acces direct = plus rapide 
	file=open(pathMain+pinList[pin]+"/value",'w') # ouvre le fichier en écriture
	file.write(state)
	file.close()
	


# digitalRead
def digitalRead(pin):
	
	pin=int(pin)
	
	# gpio read <pin>
	
	# lit l'etat de la broche en ligne commande avec gpio
	#cmd="gpio read "+str(pin)
	#print cmd # debug
	
	#pipe=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout 
	#state=pipe.read() # lit la sortie console
	#pipe.close() # ferme la sortie console

	#print state # debug
	
	# lit etat de la broche en acces direct 
	file=open(pathMain+pinList[pin]+"/value",'r') # ouvre le fichier en lecture
	file.seek(0) # se place au debut du fichier
	state=file.read() #lit le fichier
	file.close()
	
	return int(state)  # renvoie valeur entiere
	

def toggle(pin): # inverse l'etat de la broche
	if digitalRead(pin)==HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

#------------- Broches analogiques -----------------

# analogRead
def analogRead(pin):
	
	print("analogRead non disponible sur le RaspberryPi : passer au pcDuino !")
	
	return 0 # renvoie la valeur

# analogWrite = generation pwm
def analogWrite(pin, value): 
	
	pin=int(pin)
	value=int(rescale(value,0,255,0,1023))
	
	# fixe le mode pwm pour la broche E/S via ligne commande gpio 
	cmd="gpio mode "+str(pin)+" "+"pwm"
	subprocess.Popen(cmd, shell=True)
	print cmd # debug
	
	# gpio pwm <pin> <value> avec value entre 0 et 1023
	
	# fixe pwm via ligne commande gpio 
	cmd="gpio pwm "+str(pin)+" "+ str(value)
	subprocess.Popen(cmd, shell=True)
	print cmd # debug
	
def analogWritePercent(pin, value):
	analogWrite(pin, rescale(value,0,100,0,255)) # re-echelonne valeur 0-100% vers 0-255
	
#############################################################################
#==================== Fonctions Pyduino communes ============================
##############################################################################

################ Fonctions communes ####################

#--------> pyduinoCoreBase

######################## Fonctions Système ################################

#========= > voir pyduinoCoreSystem

######################## Fonctions Libs dédiées ################################

# classe Uart pour communication série UART 
class Uart():
	
	# def __init__(self): # constructeur principal
	
	
	def begin(self,rateIn, *arg): # fonction initialisation port serie 
		
		
		# arg = rien ou timeout ou timeout et port a utiliser
		global uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		#pinMode(RX,UART)
		#pinMode(TX,UART)
		
		#-- initialisation port serie uart 
		#try:
		if len(arg)==0: # si pas d'arguments
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
			uartPort=serial.Serial('/dev/ttyAMA0', rateIn, timeout = 10) # initialisation port serie uart
			print("Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) +" = OK ") # affiche debug
		elif len(arg)==1 : # si timeout
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
			uartPort=serial.Serial('/dev/ttyAMA0', rateIn, timeout = arg[0]) # initialisation port serie uart
			print("Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) +" = OK ") # affiche debug
			print ("timeout = " + str(arg[0] ))
		elif len(arg)==2 : # si timeout et port 
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
			uartPort=serial.Serial(arg[1], rateIn, timeout = arg[0]) # initialisation port serie uart
			print("Initialisation Port Serie : "+ arg[1] + " @ " + str(rateIn) +" = OK ") # affiche debug
			print ("timeout = " + str(arg[0] ))
		#except:
		#	print ("Erreur lors initialisation port Serie") 
			
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

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Uart = Uart() # declare instance Uart implicite 

micros0Syst=microsSyst() # mémorise microsSyst au démarrage
millis0Syst=millisSyst() # mémorise millisSyst au démarrage
