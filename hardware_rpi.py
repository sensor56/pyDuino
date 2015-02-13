############## Pyduino hardware rpi ##############

# message d'accueil
print("Pyduino for Raspberry Pi - by www.mon-club-elec.fr - 2015 ")

#### pour PWM - accès kernel + transposition C to Python ####
import fcntl # module pour fonction ioctl
import ctypes # module pour types C en Python

#### expressions regulieres ####
import re # expression regulieres pour analyse de chaines

# serie
try:
	import serial
except:
	print("ATTENTION : Module Serial manquant : installer le paquet python-serial ")

"""
#### les sous modules Pyduino utilisés par ce module ####
from CoreCommon import * # variables communes
from CoreBase import *
from CoreSystem import *
from CoreLibs import * """

# fichiers broches E/S raspberryPi
pathMain = "/sys/class/gpio/gpio"

pinList = ['17', '18', '27', '22', '23', '24', '25', '4'] # definition des borches I/O - version B
#pin=['17', '18', '21', '22', '23', '24', '25', '4'] # definition des borches I/O - version A

# constantes Arduino like
INPUT = "in"
OUTPUT = "out"
PULLUP = "up" # accepte par commande gpio

A0, A1, A2, A3, A4,A5 = 0,1,2,3,4,5 # identifiant broches analogiques
PWM0 = 1 # identifiant broches PWM


############## Broche logique ##############

# export
def export(pin):
	try:
		file = open(pathMain + "/export", 'w')
		file.write(pinList[pin])
		file.close()
	except:
		print("ERREUR : Impossible d'ouvrir la broche")
		return -1
	else:
		return 0

# pinMode 
def pinMode(pin, mode):
	pin = int(pin) # numéro de la broche (int)
	mode = str(mode) # mode de fonctionnement (str)
	
	if export(pin) == 0:
		# gpio mode <pin> in/out/pwm/clock/up/down/tri
		if mode == INPUT or mode == OUTPUT : # si in ou out 
			# en acces direct = plus rapide 
			try:
				file = open(pathMain + "gpio" + pinList[pin] + "/direction",'w') # ouvre le fichier en écriture
				file.write(OUTPUT)
				file.close()
			except:
				print("ERREUR : Impossible d'orienté la broche")
				return -1
			else:
				return 0

		elif mode == PULLUP : # sinon = si up
			# fixe le mode de la broche E/S via ligne commande gpio 
			cmd = "gpio mode " + str(pin) + " " + mode
			subprocess.Popen(cmd, shell = True)
			print(cmd) # debug

		return 0

	else:
		return -1


############## Broche logique ##############

# digitalWrite 
def digitalWrite(pin, state):
	pin = int(pin)
	state = str(state) # transforme en chaine
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	# met la broche dans etat voulu via ligne de commande gpio
	#cmd="gpio write "+str(pin)+" "+str(state)
	#subprocess.Popen(cmd, shell=True)	
	#print cmd # debug
	
	# en acces direct = plus rapide 
	try:
		file = open(pathMain + "gpio" + pinList[pin] + "/value",'w') # ouvre le fichier en écriture
		file.write(state)
		file.close()
	except:
		print("ERREUR : Impossible d'ecrire sur la broche")
		return -1
	else:
		return 0

# digitalRead
def digitalRead(pin):
	pin = int(pin)

    try:
		# lit etat de la broche en acces direct 
		file = open(pathMain + "gpio" + pinList[pin] + "/value",'r') # ouvre le fichier en lecture
		file.seek(0) # se place au debut du fichier
		state = file.read() #lit le fichier
		file.close()
	except:
		print("ERREUR : Impossible de lire la broche")
		return -1
	else:
		return int(state)  # renvoie valeur entiere

def toggle(pin): # inverse l'etat de la broche
	if digitalRead(pin) == HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

############## Broche analogique ##############

# analogRead
def analogRead(pin):
	print("ERREUR : analogRead non disponible sur le RaspberryPi")
	return 0 # renvoie la valeur

# analogWrite = generation pwm
def analogWrite(pin, value): 
	pin = int(pin)
	value = int(rescale(value,0,255,0,1023))
	
	# fixe le mode pwm pour la broche E/S via ligne commande gpio 
	cmd = "gpio mode " + str(pin) + " " + "pwm"
	subprocess.Popen(cmd, shell=True)
	print(cmd) # debug
	
	# gpio pwm <pin> <value> avec value entre 0 et 1023
	
	# fixe pwm via ligne commande gpio 
	cmd = "gpio pwm " + str(pin) + " " + str(value)
	subprocess.Popen(cmd, shell=True)
	print(cmd) # debug
	
def analogWritePercent(pin, value):
	analogWrite(pin, rescale(value,0,100,0,255)) # re-echelonne valeur 0-100% vers 0-255
	

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
		if len(arg) == 0: # si pas d'arguments
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
			uartPort = serial.Serial('/dev/ttyAMA0', rateIn, timeout = 10) # initialisation port serie uart
			print("Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) + " = OK ") # affiche debug
		elif len(arg) == 1 : # si timeout
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
			uartPort = serial.Serial('/dev/ttyAMA0', rateIn, timeout = arg[0]) # initialisation port serie uart
			print("Initialisation Port Serie : /dev/ttyAMA0 @ " + str(rateIn) + " = OK ") # affiche debug
			print("timeout = " + str(arg[0] ))
		elif len(arg) == 2 : # si timeout et port 
			#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
			uartPort=serial.Serial(arg[1], rateIn, timeout = arg[0]) # initialisation port serie uart
			print("Initialisation Port Serie : " + arg[1] + " @ " + str(rateIn) + " = OK ") # affiche debug
			print("timeout = " + str(arg[0] ))
		#except:
		#	print ("Erreur lors initialisation port Serie") 
			
	def println(self,text, *arg):  # message avec saut de ligne
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
				out=bin(int(text))
				#print(out) # debug
			elif arg[0] == OCT and text.isdigit():
				out=oct(int(text))
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

########################### --------- initialisation ------------ #################

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Uart = Uart() # declare instance Uart implicite 

micros0Syst = microsSyst() # mémorise microsSyst au démarrage
millis0Syst = millisSyst() # mémorise millisSyst au démarrage
