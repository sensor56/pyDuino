#!/usr/bin/python
# -*- coding: utf-8 -*-

# Par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

# message d'accueil 
print "Pyduino for pcDuino - by www.mon-club-elec.fr - 2015 "


### Expressions regulieres ###
import re # Expression regulieres pour analyse de chaines

# Serie Uart
try:
	import serial
except: 
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

### Module des variables communes partagées entre les éléments Pyduino ###
import coreCommon as common

### Declarations ###
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop ou de passer par un fichier commun... 

# sur le pcDuino, la plupart des operations passent par des fichiers systeme
# important : pour réaffecter la valeur d'une variable partagée = IL FAUT UTILISER LE NOM DU MODULE - sinon variable globale module, pas partagée... 

common.PLATFORM = "PCDUINO"

# Fichiers broches E/S pcDuino
common.pathMode  = "/sys/devices/virtual/misc/gpio/mode/"
common.pathState = "/sys/devices/virtual/misc/gpio/pin/"

# onstantes Arduino like spécifique de la plateforme utilisée 
common.INPUT  = "0"
common.OUTPUT = "1"
common.PULLUP = "8"

common.A0, common.A1, common.A2, common.A3, common.A4,common.A5 = 0,1,2,3,4,5 # Identifiant broches analogiques
common.PWM = [3,5,6,9,10,11] # List pour acces par indice
common.PWM0, common.PWM1, common.PWM2, common.PWM3, common.PWM4,common.PWM5 = common.PWM[0],common.PWM[1],common.PWM[2],common.PWM[3],common.PWM[4],common.PWM[5] # identifiant broches PWM


### Les sous modules Pyduino utilisés par ce module - à mettre après les variables spécifiques ci-dessus ###
from coreBase   import *
from coreSystem import *
from coreLibs   import *
### Pour PWM - accès kernel + transposition C to Python ###
import fcntl # Module pour fonction ioctl
# from ctypes import *
import ctypes # Module pour types C en Python


# Variables globales du module 

### Pour PWM ###

# Le chemin fichier config PWM
pwm_dev = "/dev/pwmtimer"

# Les adresses registres PWM 
PWMTMR_START = 0x101
PWMTMR_STOP  = 0x102
PWMTMR_FUNC  = 0x103
PWMTMR_TONE  = 0x104
PWM_CONFIG   = 0x105
HWPWM_DUTY   = 0x106
PWM_FREQ     = 0x107

# Les frequences max
MAX_PWMTMR_FREQ = 2000 # 2kHz pin 3,9,10,11 
MIN_PWMTMR_FREQ = 126 # 126Hz pin 3,9,10,11 
MAX_PWMHW_FREQ  = 20000 # 20kHz pin 5,6

MAX_PWM_LEVEL = 255 # Limite max duty cycle

initPwmFlag    = [False, False, False, False, False, False] # Flags init Freq PWM - false tant que pas initialisation freq PWM
defaultPwmFreq = 520 # Frequence par defaut

### diverses classes utiles utilisées par les fonctions Pyduino ###

### pour config PWM ### 

"""	 
	 typedef struct tagPWM_Config {
    int channel;
    int dutycycle;
} PWM_Config,*pPWM_Config;
"""

class PWM_Config(ctypes.Structure):
    _fields_ = [
        ('channel', ctypes.c_int),
        ('dutycycle', ctypes.c_int)
    ]

"""
typedef struct tagPWM_Freq {
    int channel;
    int step;
    int pre_scale;
    unsigned int freq;
} PWM_Freq,*pPWM_Freq;
"""

class PWM_Freq(ctypes.Structure):
    _fields_ = [
        ('channel', ctypes.c_int),
        ('step', ctypes.c_int),
        ('pre_scale', ctypes.c_int),
        ('freq', ctypes.c_uint)
    ]


### Fonctions spécifiques pour une plateforme donnée: Version pcDuino ###

### gestion broches E/S numériques ###

# pinMode 
def pinMode(pin, mode):
	# Fixe le mode de fonctionnement de la broche
	# Mode parmi : OUTPUT, INPUT ou PULLUP
	
	pin  = int(pin) # Numéro de la broche (int)
	mode = str(mode) # Mode de fonctionnement (str)
	
	# Fixe le mode de la broche E/S
	file = open(pathMode + "gpio" + str(pin),'w') # Ouvre le fichier en ecriture
	file.write(mode) # Ecrit dans le fichier le mode voulu
	file.close()

# digitalWrite 
def digitalWrite(pin, state):
	# Met la broche dans l'état voulu
	# State parmi : HIGH ou LOW
	
	pin   = int(pin)
	state = str(state) # transforme en chaine
	
	# met la broche dans etat voulu
	file = open(pathState + "gpio" + str(pin),'w') # ouvre le fichier en ecriture
	file.write(state)
	file.close()
	

# digitalRead
def digitalRead(pin):
	# lit l'état de la broche numérique
	# renvoie int : LOW ou HIGH
	
	pin = int(pin)
	
	# lit etat de la broche 
	file = open(pathState + "gpio" + str(pin),'r') # ouvre le fichier en lecture
	file.seek(0) # se place au debut du fichier
	state = file.read()  #lit le fichier
	#print state #debug
	file.close()
	
	return int(state)  # renvoie valeur entiere
	

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
	# A0 et A1 : résolution 6 bits (0-63) en 0-2V
	# A2, A3, A4, A5 : résolution 12 bits (0-4095) en 0-3.3V
	
	pin = int(pinAnalog) # pin est un int entre 0 et 5 - utilisation identifiant predefini possible
	
	# lecture du fichier
	file = open("/proc/adc" + str(pinAnalog),'r')
	file.seek(0)  # en debut du fichier
	out = file.read() # lit la valeur = un str de la forme adc 0 : valeur
	file.close()
	
	# extraction de la valeur
	out = out.split(":") # scinde en 2 la chaine "adc 0 : valeur"
	out = out[1] # garde la 2eme partie = la valeur
	
	if debug: print out # debug
	
	#correct=5 # valeur mesure à 0V 
	correct = 0 # valeur mesure à 0V 
	
	return int(out)-correct # renvoie la valeur

### analogRead avec repetition des mesures ###
def analogReadRepeat(pinAnalogIn,repeatIn):
	
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
			mesure = rescale(mesure, 0, 4095, 0, 3300)
			#mesure=rescale(mesure,0,4095,0,3000) # en pratique, la mesure 4095 est atteinte à 3V.. 
			
	else: # forme pinAnalog, range, mV où range est la resolution et mV la tension max = qui renvoie 4095
		pinAnalog = args[0]
		rangeIn = args[1] 
		mVIn = args[2]
		
		mesure = analogRead(pinAnalog) # mesure sur la broche 
		
		mesure = rescale(mesure,0,rangeIn,0,mVIn) # en pratique, la mesure 4095 est atteinte à 3V.. 
		
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
	

# setFrequence - fixe fréquence PWM 
# D'après : https://github.com/pcduino/c_enviroment/blob/master/hardware/arduino/cores/arduino/wiring_analog.c 
# adaptation C to Python by X. HINAULT - Juin 2013
def setFrequencyPWM(pinPWMIn, frequencePWMIn):
	# broches PWM 3/9/10/11 supporte frequences[125-2000]Hz à differents dutycycle
	# broches PWM 5/6 supporte frequences [195,260,390,520,781]Hz à 256 dutycycle
	
	global initPwmFlag
	
	pin = ctypes.c_int(pinPWMIn) # broche
	freq = ctypes.c_uint(frequencePWMIn) #frequence 
	# ATTENTION : la valeur ctype ne pourra pas etre utilisee comme une valeur Python... 
	
	#print pin
	# attention : utiliser pinPWMIn pour les conditions - pin est c_type.
	
	pwmfreq = PWM_Freq() # declare objet structure
	
	if (pinPWMIn == 3 or pinPWMIn == 5 or pinPWMIn == 6 or pinPWMIn == 9 or pinPWMIn == 10 or pinPWMIn == 11) and frequencePWMIn > 0 :
		pwmfreq.channel = pin
		pwmfreq.freq = freq
		pwmfreq.step = 0
		
		# ouverture fichier
		fd = open(pwm_dev,'r')
		
		if pinPWMIn == 5 or pinPWMIn == 6 : # si broches 5 et 6 
			# pin(5/6) support frequency[195,260,390,520,781] @256 dutycycle
			if frequencePWMIn == 195 or frequencePWMIn == 260 or frequencePWMIn == 390 or frequencePWMIn == 520 or frequencePWMIn == 781: 
				ret = fcntl.ioctl(fd, PWM_FREQ, pwmfreq)  # fixe la frequence voulue 
				#initPwmFlag[pinPWMIn]=True # flag temoin config freq PWM mis à True
				initPwmFlag[PWM.index(pinPWMIn)] = frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				#print ret # debug
				if ret < 0 :
					print "Problème lors configuration PWM"
					if fd : fd.close()
					return
			else:
				print "Fréquence incompatible : choisir parmi 195,260,390,520,781 Hz"
			
		elif pinPWMIn == 3 or pinPWMIn == 9 or pinPWMIn == 10 or pinPWMIn == 11 : 
			# broches PWM 3/9/10/11 supporte frequences[125-2000]Hz à differents dutycycle
			if frequencePWMIn >= MIN_PWMTMR_FREQ and frequencePWMIn <= MAX_PWMTMR_FREQ :  # si freq entre 126 et 2000Hz
				
				# -- stop pwmtmr sur broche ---
				ret = fcntl.ioctl(fd, PWMTMR_STOP, ctypes.c_ulong(pwmfreq.channel))
				#print ret
				if ret < 0 :
					print "Probleme lors arret PWM"
					if fd : fd.close()
					return
				
				# -- fixe frequence pwm
				ret = fcntl.ioctl(fd, PWM_FREQ, pwmfreq)
				#initPwmFlag[pinPWMIn]=True # flag temoin config freq PWM mis à True
				initPwmFlag[PWM.index(pinPWMIn)] = frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				#print ret
				if ret < 0 :
					print "Probleme lors configuration PWM"
					if fd : fd.close()
					return
				
			
		
		if fd : fd.close() # ferme fichier si existe 
	else : print "Broche non autorisee pour PWM"
	

# analogWrite - sortie analogique = PWM
def analogWriteHardware(pinPWMIn, largeurIn):
	
	global initPwmFlag
		
	if initPwmFlag[PWM.index(pinPWMIn)] == False :  # si frequence PWM pas initialisee
		setFrequencyPWM(pinPWMIn,defaultPwmFreq) # utilise la frequence PWM par defaut 
	
	pin = ctypes.c_int(pinPWMIn) # broche
	value = ctypes.c_int(largeurIn)  # largeur impulsion
	
	pwmconfig = PWM_Config() # declare objet structure like C  voir classe debut code 
	
	pwmconfig.channel = pin
	pwmconfig.dutycycle = value
	
	
	if (pinPWMIn == 3 or pinPWMIn == 5 or pinPWMIn == 6 or pinPWMIn == 9 or pinPWMIn == 10 or pinPWMIn == 11) and  largeurIn >= 0 and largeurIn <= MAX_PWM_LEVEL : 
	# utiliser largeurIn car value est ctype...
		
		# ouverture fichier
		fd = open(pwm_dev,'r')
		
		if pinPWMIn == 5 or pinPWMIn == 6 : # si broches 5 et 6 
			
			# -- fixe largeur pwm
			ret = fcntl.ioctl(fd, HWPWM_DUTY, pwmconfig)
			#print ret
			if ret < 0 :
				print "Probleme lors configuration HWPWM_DUTY"
				if fd : fd.close()
				return
			
		elif pinPWMIn == 3 or pinPWMIn == 9 or pinPWMIn == 10 or pinPWMIn == 11 : 
			# -- fixe largeur pwm
			ret = fcntl.ioctl(fd, PWM_CONFIG, pwmconfig)
			#print ret
			if ret < 0 :
				print "Probleme lors configuration PWM"
				if fd : fd.close()
				return
				
			# -- démarre pwmtmr sur broche ---
			ret = fcntl.ioctl(fd, PWMTMR_START, ctypes.c_ulong(0))
			#print ret
			if ret < 0 :
				print "Probleme lors configuration PWM"
				if fd : fd.close()
				return
		
		if fd : fd.close() # ferme fichier si existe 
	else : print "Broche non autrisee pour PWM"
	

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	global initPwmFlag
	
	if initPwmFlag[PWM.index(pinPWMIn)] == False :  # si frequence PWM pas initialisee
		setFrequencyPWM(pinPWMIn,defaultPwmFreq) # utilise la frequence PWM par defaut 

	if pinPWMIn == 3 or pinPWMIn == 9 or pinPWMIn == 10 or pinPWMIn == 11: # duty natif 0-60 pour ces  broches en 520Hz
		maxDuty = int(33000 / initPwmFlag[PWM.index(pinPWMIn)]) # initPwmFlag contient la valeur de la freq courante
		
		largeurIn = rescale(largeurIn, 0, 255, 0, maxDuty) # rescale 0-255 vers 0-maxDuty
	#elif pinPWMIn==5 or pinPWMIn==6: # duty natif 0-255 pour ces 2 broches = inchangé
	
	analogWriteHardware(pinPWMIn, largeurIn) # appelle fonction utilisant largeur Hardware

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	analogWrite(pinPWMIn,rescale(largeurIn, 0, 100, 0, 255))
	

# tone
def tone(pinPWMIn, frequencyIn):
	setFrequencyPWM(pinPWMIn, frequencyIn) # modifie la fréquence - attention aux valeurs limites possibles
	analogWrite(pinPWMIn, 127) # onde 50% largeur 
	

# noTone
def noTone(pinPWMIn):
	setFrequencyPWM(pinPWMIn, 520) # restaure fréquence par défaut - et impulsion mise à 0%
	analogWrite(pinPWMIn, 0) # onde 0% largeur # pas indispensable normalement 



### Fonctions Libs dédiées ###

# et classes implémentées localement

# classe Uart pour communication série UART 
class Uart():
	
	# def __init__(self): # constructeur principal
	
	
	def begin(self, rateIn, *arg): # fonction initialisation port serie 
		
		
		# arg = rien ou timeout ou timeout et port a utiliser
		global uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		pinMode(RX,UART)
		pinMode(TX,UART)
		
		#-- initialisation port serie uart 
		try:
			if len(arg) == 0: # si pas d'arguments
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
				uartPort = serial.Serial('/dev/ttyS1', rateIn, timeout = 10) # initialisation port serie uart
				print "Initialisation Port Serie : /dev/ttyS1 @ " + str(rateIn) + " = OK " # affiche debug
			elif len(arg) == 1 : # si timeout
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort = serial.Serial('/dev/ttyS1', rateIn, timeout = arg[0]) # initialisation port serie uart
				print "Initialisation Port Serie : /dev/ttyS1 @ " + str(rateIn) + " = OK " # affiche debug
				print "timeout = " + str(arg[0])
			elif len(arg) == 2 : # si timeout et port 
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort = serial.Serial(arg[1], rateIn, timeout = arg[0]) # initialisation port serie uart
				print "Initialisation Port Serie : " + arg[1] + " @ " + str(rateIn) + " = OK " # affiche debug
				print "timeout = " + str(arg[0])
		except:
			print "Erreur lors initialisation port Serie"
			
	def println(self, text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text = str(text) # au cas où
		# print "text =" + text # debug
		
		arg = list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg) == 0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0] == DEC and text.isdigit():
				out = text
				#print(out) # debug
			elif arg[0] == BIN and text.isdigit():
				out = bin(int(text))
				#print(out) # debug
			elif arg[0] == OCT and text.isdigit():
				out = oct(int(text))
				#print(out) # debug
			elif arg[0] == HEX and text.isdigit():
				out = hex(int(text))
				#print(out) # debug
		else: # si pas de formatage de chaine = affiche tel que 
			out = text
			#print(out) # debug
		
		uartPort.write(out + chr(10)) # + saut de ligne 
		# print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		uartPort.flush()
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	
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
		
		if len(arg) == 0: endLine = "\n" # par defaut, saut de ligne
		elif len(arg) == 1: endLine = arg[0] # sinon utilise caractere voulu
		
		#-- variables de reception -- 
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = uartPort.read() # on lit le caractere
			#print charIn # debug
			
			if charIn == endLine: # si caractere fin ligne , on sort du while
				#print("caractere fin de ligne recu") # debug
				break # sort du while
			else: #tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn = chaineIn + charIn
				# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine
	
	#--- lecture de tout ce qui arrive en réception 
	def waitingAll(self): # lecture de tout en reception sur port serie 
		
		global uartPort
		
		#-- variables de reception -- 
		chaineIn = ""
		charIn = ""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn = uartPort.read() # on lit le caractere
			#print charIn # debug
			chaineIn = chaineIn + charIn
			# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn) > 0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine

# ajouter write / read   / flush 

# fin classe Uart

### initialisation ###

common.Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Serial        = common.Serial

common.Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Ethernet        = common.Ethernet # declare instance Ethernet implicite pour acces aux fonctions 

common.Uart = Uart() # declare instance Uart implicite 
Uart        = common.Uart

common.micros0Syst = microsSyst() # mémorise microsSyst au démarrage
common.millis0Syst = millisSyst() # mémorise millisSyst au démarrage