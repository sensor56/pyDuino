#!/usr/bin/python
# -*- coding: utf-8 -*-

# Par F. ILLIEN - Tous droits réservés - 2015
# www.mon-club-elec.fr - Licence GPLv3

print "Pyduino for Raspberry Pi - by www.mon-club-elec.fr - 2015 "


### Expressions regulieres ###
import re # Expression regulieres pour analyse de chaines

# Serie Uart
try:
	import serial
except:
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

"""
# reseau 
import socket 
import smtplib # serveur mail 
"""

### Module des variables communes partagées entre les éléments Pyduino ###
import CoreCommon as common

#### declarations ####
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop ou de passer par un fichier commun... 

# sur le pcDuino, la plupart des operations passent par des fichiers systeme
# important : pour réaffecter la valeur d'une variable partagée = IL FAUT UTILISER LE NOM DU MODULE - sinon variable globale module, pas partagée... 

common.PLATFORM = "RPI"

# Fichiers broches E/S raspberryPi
pathMain = "/sys/class/gpio/gpio/"

pinList = ['17', '18', '27', '22', '23', '24', '25', '4'] # Definition des borches I/O - version B
#pin=['17', '18', '21', '22', '23', '24', '25', '4'] # Definition des borches I/O - version A

A0, A1, A2, A3, A4, A5 = 0, 1, 2, 3, 4, 5 # Identifiant broches analogiques
PWM0 = 1 # Identifiant broches PWM


# Constantes Arduino like spécifique de la plateforme utilisée 
common.INPUT  = "in"
common.OUTPUT = "out"
common.PULLUP = "up" # Accepter par la commande gpio

### Les sous modules Pyduino utilisés par ce module ###
from CoreBase import *
from CoreSystem import *
from CoreLibs import *
### Pour PWM - accès kernel + transposition C to Python ###
import fcntl # Module pour fonction ioctl
import ctypes # Module pour types C en Python


### Broche logique ###

# export
def export(pin):
	try:
		file = open(pathMain + "export", 'w') # Ouvre le fichier en ecriture 
		file.write(pinList[pin]) # Ecrie le pin a exporter
		file.close()
	except:
		print "ERREUR : Impossible d'ouvrir la broche"
		return -1
	else:
		return 0

# pinMode 
def pinMode(pin, mode):
	pin  = int(pin) # Numero de la broche (int)
	mode = str(mode) # Mode de fonctionnement (str)
	
	if export(pin) == 0:
		# gpio mode <pin> in/out/pwm/clock/up/down/tri
		if mode == INPUT or mode == OUTPUT : # Si in ou out 
			# En acces direct = plus rapide 
			try:
				file = open(pathMain + "gpio" + pinList[pin] + "/direction",'w') # Ouvre le fichier en ecriture
				file.write(OUTPUT) # Ecrie l'etat du pin demande
				file.close()
			except:
				print "ERREUR : Impossible d'orienté la broche"
				return -1
			else:
				return 0

		elif mode == PULLUP : # Sinon = si up
			# Fixe le mode de la broche E/S via ligne commande gpio 
			cmd = "gpio mode " + str(pin) + " " + mode
			subprocess.Popen(cmd, shell = True)
			print cmd # debug

		return 0

	else:
		return -1


# digitalWrite 
def digitalWrite(pin, state):
	pin = int(pin)
	state = str(state) # Transforme en chaine
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	# Met la broche dans etat voulu via ligne de commande gpio
	# cmd="gpio write "+str(pin)+" "+str(state)
	# subprocess.Popen(cmd, shell=True)	
	# print cmd # debug
	
	# En acces direct = plus rapide 
	try:
		file = open(pathMain + "gpio" + pinList[pin] + "/value",'w') # Ouvre le fichier en écriture
		file.write(state)
		file.close()
	except:
		print "ERREUR : Impossible d'ecrire sur la broche"
		return -1
	else:
		return 0

# digitalRead
def digitalRead(pin):
	pin = int(pin)

    try:
		# Lit etat de la broche en acces direct 
		file = open(pathMain + "gpio" + pinList[pin] + "/value",'r') # Ouvre le fichier en lecture
		file.seek(0) # Se place au debut du fichier
		state = file.read() # Lit le fichier
		file.close()
	except:
		print "ERREUR : Impossible de lire la broche"
		return -1
	else:
		return int(state)  # Renvoie valeur entiere

def toggle(pin): # Inverse l'etat de la broche
	if digitalRead(pin) == HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

### Broche analogique ###

# analogRead
def analogRead(pin):
	print "ERREUR : analogRead non disponible sur le RaspberryPi"
	return 0 # Renvoie la valeur

# analogWrite = generation pwm
def analogWrite(pin, value): 
	pin   = int(pin)
	value = int(rescale(value,0,255,0,1023))
	
	# Fixe le mode pwm pour la broche E/S via ligne commande gpio 
	cmd = "gpio mode " + str(pin) + " " + "pwm"
	subprocess.Popen(cmd, shell=True)
	print cmd # debug
	
	# gpio pwm <pin> <value> avec value entre 0 et 1023
	
	# Fixe pwm via ligne commande gpio 
	cmd = "gpio pwm " + str(pin) + " " + str(value)
	subprocess.Popen(cmd, shell=True)
	print cmd # debug
	
def analogWritePercent(pin, value):
	analogWrite(pin, rescale(value,0,100,0,255)) # Re-echelonne valeur 0-100% vers 0-255
	

### Fonctions Libs dédiées ###

# Classe Uart pour communication série UART 
class Uart():
	# def __init__(self): # Constructeur principal
	def begin(self,rateIn, *arg): # Fonction initialisation port serie 
		# arg = rien ou timeout ou timeout et port a utiliser
		global uartPort
		
		# Configure pin 0 et 1 pour UART (mode = 3)
		# pinMode(RX,UART)
		# pinMode(TX,UART)
		
		### Initialisation port serie uart ###
		#try:
		if len(arg) == 0: # Si pas d'arguments
			# uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # Initialisation port serie uart
			uartPort = serial.Serial('/dev/ttyAMA0', rateIn, timeout = 10) # Initialisation port serie uart
			print "Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) + " = OK " # Affiche debug
		elif len(arg) == 1 : # si timeout
			# uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # Initialisation port serie uart
			uartPort = serial.Serial('/dev/ttyAMA0', rateIn, timeout = arg[0]) # Initialisation port serie uart
			print "Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) + " = OK " # Affiche debug
			print "timeout = " + str(arg[0])
		elif len(arg) == 2 : # si timeout et port 
			# uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # Initialisation port serie uart
			uartPort=serial.Serial(arg[1], rateIn, timeout = arg[0]) # Initialisation port serie uart
			print "Initialisation Port Serie : " + arg[1] + " @ " + str(rateIn) + " = OK " # Affiche debug
			print "timeout = " + str(arg[0])
		#except:
		#	print "Erreur lors initialisation port Serie" 
			
	def println(self,text, *arg):  # Message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# Attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text = str(text) # Au cas où
		# print "text =" + text # debug
		
		arg = list(arg) # Conversion en list... évite problèmes.. 
		
		# print arg - debug
		
		if not len(arg) == 0: # Si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0] == DEC and text.isdigit():
				out = text
				# print out # debug
			elif arg[0] == BIN and text.isdigit():
				out=bin(int(text))
				# print out # debug
			elif arg[0] == OCT and text.isdigit():
				out=oct(int(text))
				# print out # debug
			elif arg[0] == HEX and text.isdigit():
				out = hex(int(text))
				# print out # debug
		else: # Si pas de formatage de chaine = affiche tel que 
			out = text
			# print out # debug
		
		uartPort.write(out + chr(10)) # + saut de ligne 
		# print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		uartPort.flush()
		# Ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# Si type est long ou int
	
	
	def available(self):
		global uartPort
		
		if uartPort.inWaiting(): 
			return True
		else: 
			return False
		
	def flush(self):
		global uartPort
		return uartPort.flush()
	
	def read(self):
		global uartPort
		return uartPort.read()
	
	def write(self, strIn):
		global uartPort
		uartPort.write(strIn)
		
	
	
	### Lecture d'une ligne jusqu'a caractere de fin indique ###
	def waiting(self, *arg): # Lecture d'une chaine en reception sur port serie 
		global uartPort
		
		if len(arg) == 0: endLine = "\n" # Par defaut, saut de ligne
		elif len(arg) == 1: endLine = arg[0] # Sinon utilise caractere voulu
		
		### Variables de reception ###
		chaineIn = ""
		charIn = ""
		
		# delay(20) # Laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # Tant que au moins un caractere en reception
			charIn = uartPort.read() # On lit le caractere
			# print charIn # debug
			
			if charIn == endLine: # Si caractere fin ligne , on sort du while
				# print("Caractere fin de ligne recu") # debug
				break # Sort du while
			else: # Tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn = chaineIn + charIn
				# print chaineIn # debug
			
		### Une fois sorti du while : on se retrouve ici - attention indentation ###
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			# print(chaineIn) # Affiche la chaine # debug
			return chaineIn  # Renvoie la chaine 
		else:
			return False # Si pas de chaine
	
	### Lecture de tout ce qui arrive en réception ###
	def waitingAll(self): # Lecture de tout en reception sur port serie 
		global uartPort
		
		### Variables de reception ###
		chaineIn = ""
		charIn = ""
		
		# delay(20) # Laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # Tant que au moins un caractere en reception
			charIn = uartPort.read() # On lit le caractere
			# print charIn # debug
			chaineIn = chaineIn + charIn
			# print chaineIn # debug
			
		### Une fois sorti du while : on se retrouve ici - attention indentation ###
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # Affiche la chaine # debug
			return chaineIn  # Renvoie la chaine 
		else:
			return False # Si pas de chaine

# Ajouter write / read   / flush

### Initialisation###

Serial   = Serial() # Declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet() # Declare instance Ethernet implicite pour acces aux fonctions 
Uart     = Uart() # Declare instance Uart implicite 

micros0Syst = microsSyst() # Mémorise microsSyst au démarrage
millis0Syst = millisSyst() # Mémorise millisSyst au démarrage