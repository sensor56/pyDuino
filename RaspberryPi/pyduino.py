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

# sur le raspberryPi, la plupart des operations sont accessible vaec la commande gpio 

# fichiers broches E/S raspberryPi
pathMain="/sys/class/gpio/gpio"

# constantes Arduino like
INPUT="in"
OUTPUT="out"
PULLUP="up"

HIGH = 1
LOW =  0

A0, A1, A2, A3, A4,A5 =0,1,2,3,4,5 # identifiant broches analogiques
PWM0=1 # identifiant broches PWM

# constantes Pyduino
noLoop=False 

# --- fonctions Arduino ---- 

# pinMode 
def pinMode(pin, mode):
	
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	# fixe le mode de la broche E/S
	cmd="gpio mode "+str(pin)+" "+mode
	subprocess.Popen(cmd, shell=True)
	print cmd # debug
	
# digitalWrite 
def digitalWrite(pin, state):
	
	pin=int(pin)
	state=str(state) # transforme en chaine
	
	# gpio mode <pin> in/out/pwm/clock/up/down/tri
	
	# met la broche dans etat voulu
	cmd="gpio write "+str(pin)+" "+str(state)
	subprocess.Popen(cmd, shell=True)	
	#print cmd # debug


# digitalRead
def digitalRead(pin):
	
	pin=int(pin)
	
	# gpio read <pin>
	
	# lit l'etat de la broche
	cmd="gpio read "+str(pin)
	print cmd # debug
	
	pipe=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout 
	state=pipe.read() # lit la sortie console
	pipe.close() # ferme la sortie console

	print state # debug
	
	return int(state)  # renvoie valeur entiere
	

# analogRead
def analogRead(pin):
	
	print("analogRead non disponible sur le RaspberryPi : passer au pcDuino !")
	
	return 0 # renvoie la valeur

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

# initialisation 

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal

micros0Syst=microsSyst() # mémorise microsSyst au démarrage
millis0Syst=millisSyst() # mémorise millisSyst au démarrage
