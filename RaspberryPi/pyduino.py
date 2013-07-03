#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

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
# modules utiles 
import time
import subprocess

# import math
from math import *  # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()

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

HIGH = 1
LOW =  0

A0, A1, A2, A3, A4,A5 =0,1,2,3,4,5 # identifiant broches analogiques
PWM0=1 # identifiant broches PWM

# constantes Pyduino
noLoop=False 

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
	# Renvoie l'octet de poids faible de la valeur a
	
	
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	out=out[-8:] # extrait 8 derniers caracteres - LSB a droite / MSB a gauche 
	while len(out)<8:out="0"+out # complete jusqu'a 8 O/1
	out="0b"+out # re-ajoute 0b 
	return out

def highByte(a):
	# renvoie l'octet de poids fort de la valeur a
	
	
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	while len(out)>8:out=out[:-8] # tant que plus de 8 chiffres, enleve 8 par 8 = octets low

	# une fois obtenu le highbyte, on complete les 0 jusqu'a 8 chiffres
	while len(out)<8:out="0"+out # complete jusqu'a 8 O/1
	out="0b"+out # re-ajoute 0b 
	return out
	

def bitRead(a, index):
	# lit le bit de rang index de la valeur a
	# le bit de poids faible a l'index 0
	
	out=bin(a) # '0b1011000101100101'
	out=out[2:] # enleve 0b '1011000101100101'
	out=out[len(out)-index-1] # rang le plus faible = indice 0 = le plus a droite
	# extrait le caractere du bit voulu - LSB a droite / MSB a gauche 
	#out="0b"+out # re-ajoute 0b 
	return out
	

def bitWrite(a, index, value):
	# Met le bit d'index voulu de la valeur a a la valeur indiquee (HIGH ou LOW)
	# le bit de poids faible a l'index 0 
	
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
	# Met le bit d'index voulu de la valeur a a HIGH
	# le bit de poids faible a l'index 0
	
	return bitWrite(a,index,1) # met le bit voulu a 1 - Index 0 pour 1er bit poids faible
	

def bitClear(a,index):
	# Met le bit d'index voulu de la valeur a a LOW
	# le bit de poids faible a l'index 0 
	
	return bitWrite(a,index,0) # met le bit voulu a 0 - Index 0 pour 1er bit poids faible
	

def bit(index): # calcule la valeur du bit d'index specifie (le bits LSB a l'index 0)
	# calcule la valeur du bit d'index specifie 
	# le bits de poids faible a l'index 0 - calcule en fait 2 exposant index
	
	return pow(2,index) # cette fonction renvoie en fait la valeur 2^index
	

######################## Fonctions par thèmes ################################

#-- Console -- 

# classe Serial pour émulation affichage message en console
class Serial():
	
	# def __init__(self): # constructeur principal
	
	def println(self,text, *arg):  # message avec saut de ligne
		# Emulation Serial.println dans console systeme
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text=str(text) # au cas où
		
		arg=list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg)==0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0]==DEC and text.isdigit():
				print(text)
			elif arg[0]==BIN and text.isdigit():
				print(bin(int(text)))
			elif arg[0]==OCT and text.isdigit():
				print(oct(int(text)))
			elif arg[0]==HEX and text.isdigit():
				print(hex(int(text)))
		else: # si pas de formatage de chaine = affiche tel que 
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

########################### initialisation ########################

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal

micros0Syst=microsSyst() # mémorise microsSyst au démarrage
millis0Syst=millisSyst() # mémorise millisSyst au démarrage
