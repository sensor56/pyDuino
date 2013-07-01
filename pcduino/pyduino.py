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

Ce fichier est la version 0.1c pour le pcDuino
"""

# modules utiles 

#-- temps --
import time

#-- math -- 
# import math
from math import *  # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()

#-- pour PWM - accès kernel + transposition C to Python -- 
import fcntl # module pour fonction ioctl
#from ctypes import *
import ctypes # module pour types C en Python 

# -- declarations --
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop


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
PWM0, PWM1, PWM2, PWM3, PWM4,PWM5 =3,5,6,9,10,11 # identifiant broches PWM

# constantes utiles pyDuino
noLoop=False # pour stopper loop

# -- pour PWM --

# le chemin fichier config PWM
pwm_dev = "/dev/pwmtimer"

# les adresses registres PWM 
PWMTMR_START =0x101
PWMTMR_STOP =0x102
PWMTMR_FUNC=0x103
PWMTMR_TONE =0x104
PWM_CONFIG=0x105
HWPWM_DUTY=0x106
PWM_FREQ=0x107

# Les frequences max
MAX_PWMTMR_FREQ=2000 # 2kHz pin 3,9,10,11 
MIN_PWMTMR_FREQ=126 # 126Hz pin 3,9,10,11 
MAX_PWMHW_FREQ=20000 # 20kHz pin 5,6

MAX_PWM_LEVEL=255 # limite max duty cycle

initPwmFlag=[False,False,False,False,False, False] # flags init Freq PWM - false tant que pas initialisation freq PWM
defaultPwmFreq=520 # frequence par defaut

#==== diverses classes utiles utilisées par les fonctions Pyduino ===

# -- pour config PWM -- 

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


# ==================== Fonctions spécifiques pour une plateforme donnée =============================
# =====================>>>>>>>>>> version pcDuino <<<<<<<<<<< =======================================


# ---- gestion broches E/S numériques ---

# pinMode 
def pinMode(pin, mode):
	# fixe le mode de fonctionnement de la broche
	# mode parmi : OUTPUT, INPUT ou PULLUP
	
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# fixe le mode de la broche E/S
	file=open(pathMode+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(mode) # ecrit dans le fichier le mode voulu
	file.close()

# digitalWrite 
def digitalWrite(pin, state):
	# met la broche dans l'état voulu
	# state parmi : HIGH ou LOW
	
	pin=int(pin)
	state=str(state) # transforme en chaine
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(state)
	file.close()
	

# digitalRead
def digitalRead(pin):
	# lit l'état de la broche numérique
	# renvoie int : LOW ou HIGH
	
	pin=int(pin)
	
	# lit etat de la broche 
	file=open(pathState+"gpio"+str(pin),'r') # ouvre le fichier en lecture
	file.seek(0) # se place au debut du fichier
	state=file.read()  #lit le fichier
	#print state #debug
	file.close()
	
	return int(state)  # renvoie valeur entiere
	

#----- gestion broches analogique -----

# analogRead - entrées analogiques 
def analogRead(pinAnalog):
	# A0 et A1 : résolution 6 bits (0-63) en 0-2V
	# A2, A3, A4, A5 : résolution 12 bits (0-4095) en 0-3.3V
	
	pin=int(pin) # pin est un int entre 0 et 5 - utilisation identifiant predefini possible
	
	# lecture du fichier
	file=open('/proc/adc'+str(pinAnalog),'r')
	file.seek(0)  # en debut du fichier
	out=file.read() # lit la valeur = un str de la forme adc 0 : valeur
	file.close()
	
	# extraction de la valeur
	out=out.split(":") # scinde en 2 la chaine "adc 0 : valeur"
	out=out[1] # garde la 2eme partie = la valeur
	
	return int(out) # renvoie la valeur

# setFrequence - fixe fréquence PWM 
# D'après : https://github.com/pcduino/c_enviroment/blob/master/hardware/arduino/cores/arduino/wiring_analog.c 
# adaptation C to Python by X. HINAULT - Juin 2013
def setFrequencyPWM(pinPWMIn, frequencePWMIn):
	# broches PWM 3/9/10/11 supporte frequences[125-2000]Hz à differents dutycycle
	# broches PWM 5/6 supporte frequences [195,260,390,520,781]Hz à 256 dutycycle
	
	global initPwmFlag
	
	pin=ctypes.c_int(pinPWMIn) # broche
	freq=ctypes.c_uint(frequencePWMIn) #frequence 
	# ATTENTION : la valeur ctype ne pourra pas etre utilisee comme une valeur Python... 
	
	print pin
	# attention : utiliser pinPWMIn pour les conditions - pin est c_type.
	
	pwmfreq = PWM_Freq() # declare objet structure
	
	if (pinPWMIn==3 or pinPWMIn==5 or pinPWMIn==6 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11) and frequencePWMIn>0 :
		pwmfreq.channel=pin
		pwmfreq.freq=freq
		pwmfreq.step=0
		
		# ouverture fichier
		fd=open(pwm_dev,'r')
		
		if pinPWMIn==5 or pinPWMIn==6 : # si broches 5 et 6 
			# pin(5/6) support frequency[195,260,390,520,781] @256 dutycycle
			if frequencePWMIn==195 or frequencePWMIn==260 or frequencePWMIn==390 or frequencePWMIn==520 or frequencePWMIn==781: 
				ret=fcntl.ioctl(fd, PWM_FREQ, pwmfreq)  # fixe la frequence voulue 
				#initPwmFlag[pinPWMIn]=True # flag temoin config freq PWM mis à True
				initPwmFlag[pinPWMIn]= frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				print ret # debug
				if ret<0 :
					print ("Problème lors configuration PWM")
					if fd : fd.close()
					return
			else:
				print("Fréquence incompatible : choisir parmi 195,260,390,520,781 Hz")
			
		elif pinPWMIn==3 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11 : 
			# broches PWM 3/9/10/11 supporte frequences[125-2000]Hz à differents dutycycle
			if frequencePWMIn >= MIN_PWMTMR_FREQ and frequencePWMIn <= MAX_PWMTMR_FREQ :  # si freq entre 126 et 2000Hz
				
				# -- stop pwmtmr sur broche ---
				ret=fcntl.ioctl(fd, PWMTMR_STOP, ctypes.c_ulong(pwmfreq.channel))
				print ret
				if ret<0 :
					print ("Probleme lors arret PWM")
					if fd : fd.close()
					return
				
				# -- fixe frequence pwm
				ret=fcntl.ioctl(fd, PWM_FREQ, pwmfreq)
				#initPwmFlag[pinPWMIn]=True # flag temoin config freq PWM mis à True
				initPwmFlag[pinPWMIn]= frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				print ret
				if ret<0 :
					print ("Probleme lors configuration PWM")
					if fd : fd.close()
					return
				
			
		
		if fd : fd.close() # ferme fichier si existe 
	else : print("Broche non autrisee pour PWM")
	

# analogWrite - sortie analogique = PWM
def analogWriteHardware(pinPWMIn, largeurIn):
	
	global initPwmFlag
		
	if initPwmFlag[pinPWMIn]==False :  # si frequence PWM pas initialisee
		setFrequencyPWM(pinPWMIn,defaultPwmFreq) # utilise la frequence PWM par defaut 
	
	pin=ctypes.c_int(pinPWMIn) # broche
	value=ctypes.c_int(largeurIn)  # largeur impulsion
	
	pwmconfig = PWM_Config() # declare objet structure like C  voir classe debut code 
	
	pwmconfig.channel=pin
	pwmconfig.dutycycle=value
	
	
	if (pinPWMIn==3 or pinPWMIn==5 or pinPWMIn==6 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11) and  largeurIn>=0 and largeurIn <= MAX_PWM_LEVEL : 
	# utiliser largeurIn car value est ctype...
		
		# ouverture fichier
		fd=open(pwm_dev,'r')
		
		if pinPWMIn==5 or pinPWMIn==6 : # si broches 5 et 6 
			
			# -- fixe largeur pwm
			ret=fcntl.ioctl(fd, HWPWM_DUTY, pwmconfig)
			print ret
			if ret<0 :
				print ("Probleme lors configuration HWPWM_DUTY")
				if fd : fd.close()
				return
			
		elif pinPWMIn==3 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11 : 
			# -- fixe largeur pwm
			ret=fcntl.ioctl(fd, PWM_CONFIG, pwmconfig)
			print ret
			if ret<0 :
				print ("Probleme lors configuration PWM")
				if fd : fd.close()
				return
				
			# -- démarre pwmtmr sur broche ---
			ret=fcntl.ioctl(fd, PWMTMR_START, ctypes.c_ulong(0))
			print ret
			if ret<0 :
				print ("Probleme lors configuration PWM")
				if fd : fd.close()
				return
		
		if fd : fd.close() # ferme fichier si existe 
	else : print("Broche non autrisee pour PWM")
	

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	global initPwmFlag
	
	if initPwmFlag[pinPWMIn]==False :  # si frequence PWM pas initialisee
		setFrequencyPWM(pinPWMIn,defaultPwmFreq) # utilise la frequence PWM par defaut 

	if pinPWMIn==3 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11: # duty natif 0-60 pour ces  broches en 520Hz
		maxDuty=int(33000/initPwmFlag[pinPWMIn]) # initPwmFlag contient la valeur de la freq courante
		
		largeurIn=rescale(largeurIn,0,255,0,maxDuty) # rescale 0-255 vers 0-maxDuty
	#elif pinPWMIn==5 or pinPWMIn==6: # duty natif 0-255 pour ces 2 broches = inchangé
	
	analogWriteHardware(pinPWMIn, largeurIn) # appelle fonction utilisant largeur Hardware

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	analogWrite(pinPWMIn,rescale(largeurIn,0,100,0,255))
	

################ Fonctions communes ####################

#--- temps ---
 
# delay
def delay(ms):
	int(ms)
	time.sleep(ms/1000.0) # pause en secondes

# delayMicroseconds
def delayMicroseconds(us):
	time.sleep(us/1000000.0) # pause en secondes
	
# fonction millisSyst : renvoie le nombre de millisecondes courant de l'horloge systeme
def millisSyst():
	return(int(round(time.time() * 1000))) # millisecondes de l'horloge systeme

# fonction millis : renvoie le nombre de millisecondes depuis le debut du programme
def millis():
	return millisSyst()-millis0Syst # renvoie difference entre milliSyst courant et millisSyst debut code
	

# fonction microsSyst : renvoie le nombre de microsecondes courant de l'horloge systeme
def microsSyst():
	return(int(round(time.time() * 1000000))) # microsecondes de l'horloge systeme

# fonction millis : renvoie le nombre de millisecondes depuis le debut du programme
def micros():
	return microsSyst()-micros0Syst # renvoie difference entre microsSyst courant et microsSyst debut code
	

#----------- MATH -------------

#-- min(x,y) --> Python

#-- max(x,y) --> Python

#-- abs(x) --> Python 

#-- constrain(x,a,b)
def constrain(x,valMin,valMax):
	if x < valMin : 
		return valMin

	elif valMax < x :
		return valMax

	else :
		return x

#-- map(valeur, fromLow, fromHigh, toLow, toHigh) --> renommée rescale
def rescale(valeur, in_min, in_max, out_min, out_max):
	return (valeur - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	# d'après la fonction map du fichier wirin.c du core Arduino

#-- pow(x,y) : calcul x à la puissance y --> Python

#-- sq(x) -- calcule le carré de x
def sq(x):
	return pow(x,2)

#-- sqrt(x) -- calcule la racine carrée de x --> module math
#def sqrt(x):
	#return math.sqrt(x)
	
#-- sin(x) -- sinus de l'angle en radians --> module math

#-- cos(x) cosinus de l'angle en radians --> module math

#-- tan(x) cosinus de l'angle en radians --> module math

#-- radians(x) --> module math

#-- degrees(x) --> module math

#-- randomSeed()  initialise le générateur de nombre aléatoire
def randomSeed(x):
	rd.seed(x) # appelle fonction seed du module random
	
#-- random(max) et random(min,max) : renvoie valeur aléatoire entière
def random(*arg): # soit forme random(max), soit forme random(min,max)
	if len(arg)==1:
		return rd.randint(0,arg[0])
	elif len(arg)==2:
		return rd.randint(arg[0],arg[1])
	else:
		 return 0 # si argument invalide

#-- gestion de bits et octets -- 
def lowByte(a):
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	out=out[-8:] # extrait 8 derniers caracteres - LSB a droite / MSB a gauche 
	while len(out)<8:out="0"+out # complete jusqu'a 8 O/1
	out="0b"+out # re-ajoute 0b 
	return out

def highByte(a):
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	while len(out)>8:out=out[:-8] # tant que plus de 8 chiffres, enleve 8 par 8 = octets low

	# une fois obtenu le highbyte, on complete les 0 jusqu'a 8 chiffres
	while len(out)<8:out="0"+out # complete jusqu'a 8 O/1
	out="0b"+out # re-ajoute 0b 
	return out
	

def bitRead(a, index):
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	out=out[len(out)-index-1] # rang le plus faible = indice 0 = le plus a droite
	# extrait le caractere du bit voulu - LSB a droite / MSB a gauche 
	#out="0b"+out # re-ajoute 0b 
	return out
	

def bitWrite(a, index, value):
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	out=list(out) # bascule en list
	out[len(out)-index-1]=str(value) # rang le plus faible = indice 0 = le plus a droite
	#out=str(out) # rebascule en str - pb car reste format liste
	out="".join(out) # rebascule en str - concatenation des caracteres
	# remplace le caractere du bit voulu - LSB a droite / MSB a gauche 
	out="0b"+out # re-ajoute 0b 
	return out
	

def bitSet(a,index):
	return bitWrite(a,index,1) # met le bit voulu a 1 - Index 0 pour 1er bit poids faible
	

def bitClear(a,index):
	return bitWrite(a,index,0) # met le bit voulu a 0 - Index 0 pour 1er bit poids faible
	

def bit(index): # calcule la valeur du bit d'index specifie (le bits LSB a l'index 0)
	return pow(2,index) # cette fonction renvoie en fait la valeur 2^index
	

######################## Fonctions par thèmes ################################

#-- Console -- 

# classe Serial pour émulation affichage message en console
class Serial():
	
	# def __init__(self): # constructeur principal
	
	def println(self,text):  # message avec saut de ligne
		
		text=str(text) # au cas où
		
		print(text)
		
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	"""
	def print(self,text): # affiche message sans saut de ligne
		
		#text=str(txt)
		
		print(text), # avec virgule pour affichage sans saus de ligne
	"""
	
	def begin(self,rate): # fonction pour émulation de begin... Ne fait rien... 
		return


# fin classe Serial 

########################### --------- initialisation ------------ #################

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal

micros0Syst=microsSyst() # mémorise microsSyst au démarrage
millis0Syst=millisSyst() # mémorise millisSyst au démarrage
