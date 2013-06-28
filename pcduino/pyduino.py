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

""""
Ce fichier est partie intégrante  du projet pyDuino.

pyDuino apporte une couche d'abstraction au langage Python 
afin de pouvoir utiliser les broches E/S de mini PC
avec des instructions identiques au langage Arduino

L'utilisation se veut la plus simple possible :
un seul fichier à installer. 

Ce fichier est la version pour le pcDuino
"""

# modules utiles 
import time
import math

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

# Fonctions pyDuino 

"""
def stop(): # pour arret de loop
	
	global noLoop  # globale mais dans ce module seulement... !!
	
	noLoop=True # n'a pas d'effet dans le prog principal
	print noLoop
	
"""
	
# --- fonctions Arduino ---- 

# pinMode 
def pinMode(pin, mode):
	
	pin=int(pin) # numéro de la broche (int)
	mode=str(mode) # mode de fonctionnement (str)
	
	# fixe le mode de la broche E/S
	file=open(pathMode+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(mode) # ecrit dans le fichier le mode voulu
	file.close()

# digitalWrite 
def digitalWrite(pin, state):
	
	pin=int(pin)
	state=str(state) # transforme en chaine
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'w') # ouvre le fichier en ecriture
	file.write(state)
	file.close()
	

# digitalRead
def digitalRead(pin):
	
	pin=int(pin)
	
	# met la broche dans etat voulu
	file=open(pathState+"gpio"+str(pin),'r') # ouvre le fichier en lecture
	file.seek(0) # se place au debut du fichier
	state=file.read()  #lit le fichier
	#print state #debug
	file.close()
	
	return int(state)  # renvoie valeur entiere
	

# analogRead
def analogRead(pin):
	
	pin=int(pin) # pin est un int entre 0 et 5 - utilisation identifiant predefini possible
	
	# lecture du fichier
	file=open('/proc/adc'+str(pin),'r')
	file.seek(0)  # en debut du fichier
	out=file.read() # lit la valeur = un str de la forme adc 0 : valeur
	file.close()
	
	# extraction de la valeur
	out=out.split(":") # scinde la chaine en 2
	out=out[1] # garde la 2eme partie = la valeur
	
	return int(out) # renvoie la valeur

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
	return x*x

#-- sqrt(x) -- calcule la racine carrée de x
def sqrt(x):
	return math.sqrt(x)


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
