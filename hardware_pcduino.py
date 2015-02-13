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

""""
Ce fichier est partie intégrante  du projet pyDuino.

pyDuino apporte une couche d'abstraction au langage Python 
afin de pouvoir utiliser les broches E/S de mini PC
avec des instructions identiques au langage Arduino

Ce fichier est la version pour le pcDuino
"""

# modules utiles

#-- pour PWM - accès kernel + transposition C to Python -- 
import fcntl # module pour fonction ioctl
#from ctypes import *
import ctypes # module pour types C en Python 

from pyduinoCoreCommon import * # variables communes
#from pyduino_hardware_pcduino import *
from pyduinoCoreBase import *
#from pyduinoCoreSystem import *
#from pyduinoCoreLibs import *


# variables globales du module 

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
	

def toggle(pin): # inverse l'etat de la broche
	if digitalRead(pin)==HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

def pulseOut(pin, duree): # crée une impulsion sur la broche de durée voulue
	# pin : broche
	# duree : duree du niveau INVERSE en ms
	
	if digitalRead(pin)==HIGH: # si broche au niveau HAUT
		digitalWrite(pin,LOW) # mise au niveau BAS
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,HIGH) # mise au niveau HAUT
	else: # si broche au niveau BAS
		digitalWrite(pin,HIGH) # mise au niveau HAUT
		delay(duree) # maintien le niveau la durée voulue
		digitalWrite(pin,LOW) # mise au niveau bas
	
	# cette fonction ne prétend pas à la précision à la µs près... 
	# mais a pour but d'éviter la saisie des 3 instructions en la remplaçant par une seule

#----- gestion broches analogique -----

# analogRead - entrées analogiques 
def analogRead(pinAnalog):
	# A0 et A1 : résolution 6 bits (0-63) en 0-2V
	# A2, A3, A4, A5 : résolution 12 bits (0-4095) en 0-3.3V
	
	pin=int(pinAnalog) # pin est un int entre 0 et 5 - utilisation identifiant predefini possible
	
	# lecture du fichier
	file=open('/proc/adc'+str(pinAnalog),'r')
	file.seek(0)  # en debut du fichier
	out=file.read() # lit la valeur = un str de la forme adc 0 : valeur
	file.close()
	
	# extraction de la valeur
	out=out.split(":") # scinde en 2 la chaine "adc 0 : valeur"
	out=out[1] # garde la 2eme partie = la valeur
	
	if debug: print out # debug
	
	#correct=5 # valeur mesure à 0V 
	correct=0 # valeur mesure à 0V 
	
	return int(out)-correct # renvoie la valeur

#----- analogRead avec repetition des mesures ---- 
def analogReadRepeat(pinAnalogIn,repeatIn):
	
	sommeMesures=0
	
	# réalise n mesures 
	for i in range(repeatIn): 
		sommeMesures=sommeMesures+analogRead(pinAnalogIn)
		# print i # debug 
		
	moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 
	
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
	if len(args)==1: # forme pinAnalog
		pinAnalog=args[0]
	
		mesure=analogRead(pinAnalog)
		
		if pinAnalog==A0 or pinAnalog==A1:
			mesure=rescale(mesure,0,63,0,2000)
		elif pinAnalog==A2 or pinAnalog==A3 or pinAnalog==A4 or pinAnalog==A5:
			mesure=rescale(mesure,0,4095,0,3300)
			#mesure=rescale(mesure,0,4095,0,3000) # en pratique, la mesure 4095 est atteinte à 3V.. 
			
	else: # forme pinAnalog, range, mV où range est la resolution et mV la tension max = qui renvoie 4095
		pinAnalog=args[0]
		rangeIn=args[1] 
		mVIn=args[2]
		
		mesure=analogRead(pinAnalog) # mesure sur la broche 
		
		mesure=rescale(mesure,0,rangeIn,0,mVIn) # en pratique, la mesure 4095 est atteinte à 3V.. 
		
	return mesure

#----- analogRead avec repetition des mesures ---- 
def analogReadmVRepeat(*args):
	
	# formes :
	# pinAnalogIn,repeatIn
	# pinAnalogIn,repeatIn, rangeIn, mVIn
	
	sommeMesures=0
	
	if len(args)==2: # si forme pinAnalogIn,repeatIn
		pinAnalogIn=args[0]
		repeatIn=args[1]

		# réalise n mesures avec la forme analogReadmV(pinAnalogIn) 
		for i in range(repeatIn): 
			sommeMesures=sommeMesures+analogReadmV(pinAnalogIn)
			# print i # debug 
			
		moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 
		
	else: 	# pinAnalogIn,repeatIn, rangeIn, mVIn
		pinAnalogIn=args[0]
		repeatIn=args[1]
		rangeIn=args[2]
		mVIn=args[3]
		
		# réalise n mesures avec la forme analogReadmV(pinAnalogIn, rangeIn, mVIn) 
		for i in range(repeatIn): 
			sommeMesures=sommeMesures+analogReadmV(pinAnalogIn, rangeIn, mVIn)
			# print i # debug 
			
		moyenne=float(sommeMesures)/repeatIn # calcul de la moyenne 

	return moyenne
	

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
	
	#print pin
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
				initPwmFlag[PWM.index(pinPWMIn)]= frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				#print ret # debug
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
				#print ret
				if ret<0 :
					print ("Probleme lors arret PWM")
					if fd : fd.close()
					return
				
				# -- fixe frequence pwm
				ret=fcntl.ioctl(fd, PWM_FREQ, pwmfreq)
				#initPwmFlag[pinPWMIn]=True # flag temoin config freq PWM mis à True
				initPwmFlag[PWM.index(pinPWMIn)]= frequencePWMIn # flag temoin config freq PWM mis à valeur courante freq
				#print ret
				if ret<0 :
					print ("Probleme lors configuration PWM")
					if fd : fd.close()
					return
				
			
		
		if fd : fd.close() # ferme fichier si existe 
	else : print("Broche non autorisee pour PWM")
	

# analogWrite - sortie analogique = PWM
def analogWriteHardware(pinPWMIn, largeurIn):
	
	global initPwmFlag
		
	if initPwmFlag[PWM.index(pinPWMIn)]==False :  # si frequence PWM pas initialisee
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
			#print ret
			if ret<0 :
				print ("Probleme lors configuration HWPWM_DUTY")
				if fd : fd.close()
				return
			
		elif pinPWMIn==3 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11 : 
			# -- fixe largeur pwm
			ret=fcntl.ioctl(fd, PWM_CONFIG, pwmconfig)
			#print ret
			if ret<0 :
				print ("Probleme lors configuration PWM")
				if fd : fd.close()
				return
				
			# -- démarre pwmtmr sur broche ---
			ret=fcntl.ioctl(fd, PWMTMR_START, ctypes.c_ulong(0))
			#print ret
			if ret<0 :
				print ("Probleme lors configuration PWM")
				if fd : fd.close()
				return
		
		if fd : fd.close() # ferme fichier si existe 
	else : print("Broche non autrisee pour PWM")
	

# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	global initPwmFlag
	
	if initPwmFlag[PWM.index(pinPWMIn)]==False :  # si frequence PWM pas initialisee
		setFrequencyPWM(pinPWMIn,defaultPwmFreq) # utilise la frequence PWM par defaut 

	if pinPWMIn==3 or pinPWMIn==9 or pinPWMIn==10 or pinPWMIn==11: # duty natif 0-60 pour ces  broches en 520Hz
		maxDuty=int(33000/initPwmFlag[PWM.index(pinPWMIn)]) # initPwmFlag contient la valeur de la freq courante
		
		largeurIn=rescale(largeurIn,0,255,0,maxDuty) # rescale 0-255 vers 0-maxDuty
	#elif pinPWMIn==5 or pinPWMIn==6: # duty natif 0-255 pour ces 2 broches = inchangé
	
	analogWriteHardware(pinPWMIn, largeurIn) # appelle fonction utilisant largeur Hardware

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	analogWrite(pinPWMIn,rescale(largeurIn,0,100,0,255))
	

# tone
def tone(pinPWMIn,frequencyIn):
	setFrequencyPWM(pinPWMIn, frequencyIn) # modifie la fréquence - attention aux valeurs limites possibles
	analogWrite(pinPWMIn,127) # onde 50% largeur 
	

# noTone
def noTone(pinPWMIn):
	setFrequencyPWM(pinPWMIn, 520) # restaure fréquence par défaut - et impulsion mise à 0%
	analogWrite(pinPWMIn,0) # onde 0% largeur # pas indispensable normalement 
