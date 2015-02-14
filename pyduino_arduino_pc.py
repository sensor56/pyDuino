#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

# message d'accueil 
print "Pyduino for PC Desktop with Arduino - v0.5dev - by www.mon-club-elec.fr - 2014 "


### expressions regulieres ###
import re # expression regulieres pour analyse de chaines

# serie Uart
try:
	import serial
except: 
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

"""
# reseau 
import socket 
import smtplib # serveur mail 
"""

### module des variables communes partagées entre les éléments Pyduino ###
import CoreCommon as common

### declarations ###
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop

common.PLATFORM = "ARDUINOPC"

# constantes Arduino like
common.INPUT  = "0"
common.OUTPUT = "1"
common.PULLUP = "8"

# pour uart
#UART="3"
#RX=0
#TX=1

common.A0, common.A1, common.A2, common.A3, common.A4, common.A5 = 0, 1, 2, 3, 4, 5 # identifiant broches analogiques
common.PWM0, common.PWM1, common.PWM2, common.PWM3, common.PWM4,common.PWM5 = 3, 5, 6, 9, 10, 11 # identifiant broches PWM



### les sous modules Pyduino utilisés par ce module - à mettre après les variables spécifiques ci-dessus ###
from CoreBase import *
from CoreSystem import *
from CoreLibs import *

# variables globales du module 


### Fonctions spécifiques pour une plateforme donnée: version Arduino + PC ###

### gestion broches E/S numériques ---

# pinMode 
def pinMode(pin, mode):
	if mode == OUTPUT : 
		common.Uart.println("pinMode(" + str(pin) + ",1)") # envoi commande - attention OUTPUT c'est 1
		
		out = None
		while not out : # attend reponse 
			out = common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode == INPUT : 
		out = None
		while not out : # tant que pas de reponse envoie une requete
			common.Uart.println("pinMode(" + str(pin) + ",0)") # attention input c'est 0
			#print ("pinMode("+str(pin)+",0)") # debug 
			
			out = common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode == PULLUP : 
		common.Uart.println("pinMode(" + str(pin) + ",0)") # attention INPUT c'est 0
		delay(100) # laisse temps reponse arriver
		print "pinMode(" + str(pin) + ",0)"
		
		out = None
		while not out : # attend reponse
			out = common.Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
		digitalWrite(pin,HIGH) # activation du pullup 
	
# digitalWrite 
def digitalWrite(pin, state):
	common.Uart.println("digitalWrite(" + str(pin) + "," + str(state) + ")") # 
	#print ("digitalWrite("+str(pin)+","+str(state)+")") # debug

# digitalRead
def digitalRead(pin):
	# envoi de la commande
	common.Uart.println("digitalRead(" + str(pin) + ")") 
	print "digitalRead(" + str(pin) + ")"
	# attend un reponse
	out = None
	while not out : # tant que pas de reponse envoie une requete
		out = common.Uart.waiting() # lit les caracteres
	
	print out # debug
	#out=out.splitlines()
	
	return out # renvoie la valeur



def toggle(pin): # inverse l'etat de la broche
	
	
	
	if digitalRead(pin) == HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

def pulseOut(pin, duree): # crée une impulsion sur la broche de durée voulue
	# pin : broche
	# duree : duree du niveau INVERSE en ms
	
	if digitalRead(pin) == HIGH: # si broche au niveau HAUT
		digitalWrite(pin,LOW) # mise au niveau BAS
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,HIGH) # mise au niveau HAUT
	else: # si broche au niveau BAS
		digitalWrite(pin,HIGH) # mise au niveau HAUT
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,LOW) # mise au niveau bas
	
	# cette fonction ne prétend pas à la précision à la µs près... 
	# mais a pour but d'éviter la saisie des 3 instructions en la remplaçant par une seule

### gestion broches analogique ###

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
	common.Uart.println("analogRead(" + str(pinAnalog) + ")") # 
	
	# attend une réponse 
	out = None
	while not out : # tant que pas de reponse 
		#print ("analogRead("+str(pinAnalog)+")") # debug
		#delay(50) # attend reponse
		out = common.Uart.waiting() # lit les caracteres
	
	if debug: print out # debug
	
	outlines = out.splitlines() # extrait les lignes... une manière simple de supprimer le fin de ligne
	if outlines[0].isdigit() :
		return int(outlines[0]) # renvoie la valeur
	else:
		return(-1)	

### analogRead avec repetition des mesures ### 
def analogReadRepeat(pinAnalogIn, repeatIn):
	sommeMesures = 0
	
	# réalise n mesures 
	for i in range(repeatIn): 
		sommeMesures = sommeMesures + analogRead(pinAnalogIn)
		# print i # debug 
		
	moyenne = float(sommeMesures) / repeatIn # calcul de la moyenne 
	
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
	if len(args) == 1: # forme pinAnalog
		pinAnalog = args[0]
	
		mesure = analogRead(pinAnalog)
		
		if pinAnalog == A0 or pinAnalog == A1:
			mesure = rescale(mesure, 0, 63, 0, 2000)
		elif pinAnalog == A2 or pinAnalog == A3 or pinAnalog == A4 or pinAnalog == A5:
			#mesure=rescale(mesure,0,4095,0,3300)
			mesure = rescale(mesure, 0, 4095, 0, 3000) # en pratique, la mesure 4095 est atteinte à 3V.. 
			
	else: # forme pinAnalog, range, mV où range est la resolution et mV la tension max = qui renvoie 4095
		pinAnalog = args[0]
		rangeIn = args[1] 
		mVIn = args[2]
		
		mesure = analogRead(pinAnalog) # mesure sur la broche 
		
		mesure = rescale(mesure, 0, rangeIn, 0, mVIn) # en pratique, la mesure 4095 est atteinte à 3V.. 
		
	return mesure

### analogRead avec repetition des mesures ###
def analogReadmVRepeat(*args):
	# formes :
	# pinAnalogIn,repeatIn
	# pinAnalogIn,repeatIn, rangeIn, mVIn
	
	sommeMesures = 0
	
	if len(args) == 2: # si forme pinAnalogIn,repeatIn
		pinAnalogIn = args[0]
		repeatIn = args[1]

		# réalise n mesures avec la forme analogReadmV(pinAnalogIn) 
		for i in range(repeatIn): 
			sommeMesures = sommeMesures + analogReadmV(pinAnalogIn)
			# print i # debug 
			
		moyenne = float(sommeMesures) / repeatIn # calcul de la moyenne 
		
	else: 	# pinAnalogIn,repeatIn, rangeIn, mVIn
		pinAnalogIn = args[0]
		repeatIn = args[1]
		rangeIn = args[2]
		mVIn = args[3]
		
		# réalise n mesures avec la forme analogReadmV(pinAnalogIn, rangeIn, mVIn) 
		for i in range(repeatIn): 
			sommeMesures = sommeMesures + analogReadmV(pinAnalogIn, rangeIn, mVIn)
			# print i # debug 
			
		moyenne = float(sommeMesures) / repeatIn # calcul de la moyenne 

	return moyenne
	

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	Uart.println("analogWrite(" + str(pinPWMIn) + "," + str(largeurIn) + ")") # 
	print "analogWrite("+str(pinPWMIn) + "," + str(largeurIn) + ")" # debug 

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	global uartPort
	
	if not uartPort : 
		Uart.begin(115200)

	analogWrite(pinPWMIn,rescale(largeurIn, 0, 100, 0, 255))
	

# tone
def tone(pinPWMIn,frequencyIn):
	setFrequencyPWM(pinPWMIn, frequencyIn) # modifie la fréquence - attention aux valeurs limites possibles
	analogWrite(pinPWMIn, 127) # onde 50% largeur 
	

# noTone
def noTone(pinPWMIn):
	setFrequencyPWM(pinPWMIn, 520) # restaure fréquence par défaut - et impulsion mise à 0%
	analogWrite(pinPWMIn, 0) # onde 0% largeur # pas indispensable normalement 
	


### Fonctions Libs dédiées ###

# classe Uart pour communication série UART - avant import 

# uartPort=None # objet global  => common

class Uart():
	
	#def __init__(self): # constructeur principal
	#	return
	
	
	def begin(self, rateIn, *arg): # fonction pour émulation de begin... Ne fait rien... 
		
		#global common.uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		#pinMode(RX,UART) - sur le pcduino
		#pinMode(TX,UART)
		
		### initialisation port serie uart ### 
		try:
			if len(arg) == 0: # si pas d'arguments
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
				#uartPort=serial.Serial('/dev/ttyACM0', rateIn, timeout = 10) # initialisation port serie uart
				common.uartPort = serial.Serial('/dev/ttyACM0', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 10)
				common.uartPort.flushInput() # vide la file d'attente série
			if len(arg) == 1 : # si timeout
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				common.uartPort = serial.Serial('/dev/ttyACM0', rateIn, timeout = arg[0]) # initialisation port serie uart
				common.uartPort.flushInput() # vide la file d'attente série
				
			print "Initialisation Port Serie : /dev/ttyACM0 @ " + str(rateIn) + " = OK ") # affiche debug
			
		except:
			print "Erreur lors initialisation port Serie" 
			
	def waitOK(self): # fonction pour attendre reponse OK suite initialisation
		out = None
		while not out : # attend une réponse 
			out = Uart.waitingAll() # lit tous les caracteres
		
		print out
	
	
	def println(self,text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		#global common.uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text = str(text) # au cas où
		
		arg = list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg) == 0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0] == DEC and text.isdigit():
				# print(text)
				out = text
			elif arg[0] == BIN and text.isdigit():
				out = bin(int(text))
				# print(out)
			elif arg[0] == OCT and text.isdigit():
				out = oct(int(text))
				# print(out)
			elif arg[0] == HEX and text.isdigit():
				out = hex(int(text))
				# print(out)
		else: # si pas de formatage de chaine = affiche tel que 
			out = text
			# print(out)
		
		common.uartPort.write(out + chr(10)) # + saut de ligne 
		#print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	"""
	def print(self,text): # affiche message sans saut de ligne
		
		#text=str(txt)
		
		print(text), # avec virgule pour affichage sans saus de ligne
	"""
	
	def available(self):
		#global common.uartPort
		
		if common.uartPort.inWaiting() : return True
		else: return False
		
	def flush(self):
		#global common.uartPort
		return common.uartPort.flush()
	
	def read(self):
		#global common.uartPort
		return common.uartPort.read()
	
	def write(self, strIn):
		#global common.uartPort
		common.uartPort.write(strIn)
		
	### lecture d'une ligne jusqu'a caractere de fin indique ###
	def waiting(self, *arg): # lecture d'une chaine en reception sur port serie 
		
		#global common.uartPort
		
		if len(arg) == 0: endLine = "\n" # par defaut, saut de ligne
		elif len(arg) == 1: endLine = arg[0] # sinon utilise caractere voulu
		
		### variables de reception ### 
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while common.uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = common.uartPort.read() # on lit le caractere
			#print charIn # debug
			
			if charIn == endLine: # si caractere fin ligne , on sort du while
				#print("caractere fin de ligne recu") # debug
				break # sort du while
			else: #tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn = chaineIn + charIn
				# print chaineIn # debug
			
		### une fois sorti du while : on se retrouve ici - attention indentation ###
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine
	
	### lecture de tout ce qui arrive en réception ###
	def waitingAll(self): # lecture de tout en reception sur port serie 
		
		#global common.uartPort
		
		### variables de reception ###
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while common.uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = common.uartPort.read() # on lit le caractere
			#print charIn # debug
			chaineIn = chaineIn + charIn
			# print chaineIn # debug
			
		### une fois sorti du while : on se retrouve ici - attention indentation ###
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine


# fin classe Uart

### initialisation ####

common.Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Serial        = common.Serial

common.Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Ethernet        = common.Ethernet

common.Uart = Uart() # declare instance Uart implicite 
Uart        = common.Uart
#print Uart # debug

common.micros0Syst = microsSyst() # mémorise microsSyst au démarrage
common.millis0Syst = millisSyst() # mémorise millisSyst au démarrage


# initialisation port série dès le début car va communiquer ave Arduino
Uart.begin(115200) # initialise comm' série 
delay(3000) # laisse le temps à la réponse d'arriver
Uart.waitOK() # attend réponse port serie OK 