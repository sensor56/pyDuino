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

Ce fichier contient les fonctions communes de librairies dédiées (SPI, I2C, Servomoteurs, etc..) pour toutes les versions

"""

# -- importe les autres modules Pyduino
from pyduinoCoreCommon import * # variables communes

if PLATFORM=="PCDUINO" : 
	print "PCDUINO"
	from pyduino_hardware_pcduino import *
if PLATFORM=="ARDUINOPC" : 
	print "ARDUINOPC"
	from pyduino_hardware_arduino_pc import *

from pyduinoCoreBase import *
from pyduinoCoreSystem import *
#from pyduinoCoreLibs import *

################### Liquid Crystal ##################

# "registres" de base
LCD_FUNCTIONSET=0x20
LCD_DISPLAYCONTROL=0x08
LCD_ENTRYMODESET=0x04
LCD_SETDDRAMADDR=0x80
LCD_CURSORSHIFT=0x10

# bits de configuration générale
LCD_4BITMODE=0x00
LCD_5x8DOTS=0x00
LCD_2LINE=0x08
LCD_1LINE=0x00

# bits config d'affichage curseur 
LCD_DISPLAYON=0x04
LCD_DISPLAYOFF=0x00
LCD_CURSORON=0x02
LCD_CURSOROFF=0x00
LCD_BLINKON =0x01
LCD_BLINKOFF=0x00

# bits config display entry mode
LCD_ENTRYRIGHT=0x00
LCD_ENTRYLEFT=0x02
LCD_ENTRYSHIFTINCREMENT=0x01
LCD_ENTRYSHIFTDECREMENT=0x00

# bits config mouvement 
LCD_DISPLAYMOVE=0x08
LCD_CURSORMOVE=0x00
LCD_MOVERIGHT=0x04
LCD_MOVELEFT=0x00

#commandes autonomes
LCD_CLEARDISPLAY=0x01
LCD_RETURNHOME=0x02

# Class LiquiCrystal for Pyduino - by X. HINAULT - GPLv3 - Nov 2013
# adapted from LiquidCrystal Arduino library
class LiquidCrystal():

	def __init__(self,RSIn, EIn , D4In, D5In, D6In, D7In):
		
		# variables broches objet LiquidCrystal
		self.RS=RSIn
		self.E=EIn
		self.D4=D4In
		self.D5=D5In
		self.D6=D6In
		self.D7=D7In
	
		self.dataPin=[self.D7,self.D6,self.D5,self.D4] # a l'envers pour être dans même ordre que bits
		
		self.configDisplay=0x00 # variable interne drapeau affichage - se combine avec LCD_DISPLAYCONTROL
		self.configMain=0x00 # variable interne drapeau config generale - se combine avec LCD_FUNCTIONSET
		self.configEntryMode=0x00 # variable interne drapeau config generale- se combine avec LCD_ENTRYMODESET
		

	def begin(self, colonnesIn, lignesIn):
		
		self.nombreColonnes=colonnesIn
		self.nombreLignes=lignesIn
		
		# met broches utilisées en sortie 
		for pin in [self.RS,self.E,self.D4,self.D5,self.D6,self.D7]:
			pinMode(pin,OUTPUT)
		
		# RAZ initiale des broches 
		for pin in [self.RS,self.E,self.D4,self.D5,self.D6,self.D7]:
			digitalWrite(pin,LOW)
		
		# initialisation en mode 4 bits 
		delayMicroseconds(50000) # attendre au moins 40ms après ON
		
		# sequence initialisation 
		digitalWrite(self.D7,LOW)
		digitalWrite(self.D6,LOW)
		digitalWrite(self.D5,HIGH)
		digitalWrite(self.D4,HIGH)
		print("0011") # debug
		
		self.pulseEnable()
		
		delayMicroseconds(5000)  # attend 50ms
		
		digitalWrite(self.D7,LOW)
		digitalWrite(self.D6,LOW)
		digitalWrite(self.D5,HIGH)
		digitalWrite(self.D4,HIGH)
		print("0011") # debug
		
		self. pulseEnable()

		delayMicroseconds(150)  # attend 
		digitalWrite(self.D7,LOW)
		digitalWrite(self.D6,LOW)
		digitalWrite(self.D5,HIGH)
		digitalWrite(self.D4,HIGH)
		print("0011") # debug

		self.pulseEnable()
		
		delayMicroseconds(150)  # attend 
		
		# debut prise en compte effective 
		
		# set mode 4 bits 
		digitalWrite(self.D7,LOW)
		digitalWrite(self.D6,LOW)
		digitalWrite(self.D5,HIGH)
		digitalWrite(self.D4,LOW)
		print("0010") # debug
		self.pulseEnable()

		delayMicroseconds(150)  # attend 
		
		
		# instructions entières
		if self.nombreLignes>1 : self.configMain=LCD_4BITMODE|LCD_5x8DOTS|LCD_2LINE
		else: self.configMain=LCD_4BITMODE|LCD_5x8DOTS|LCD_1LINE
		#cmdInit=LCD_FUNCTIONSET|self.configMain
		# ou bit à bit ( | ) permet mise à 01 des bits voulus laissant les autres inchangés 
		self.cmd4Bits(LCD_FUNCTIONSET|self.configMain)

		self.configDisplay=LCD_DISPLAYON|LCD_CURSORON|LCD_BLINKON
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
		
		delayMicroseconds(150)  # attend 

		self.cmd4Bits(LCD_CLEARDISPLAY)
		
		self.configEntryMode=LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
		self.cmd4Bits(LCD_ENTRYMODESET|self.configEntryMode)
		
		print "----fin init----" # debug
		
	def cmd4Bits(self, cmdIn):
		
		cmdBin=bin(cmdIn)[2:].zfill(8) # convertit la commande en binaire sur 8 chiffres
		#print type(cmdBin)  #debug
		
		print cmdBin # debug
		
		digitalWrite(self.RS,LOW) # RS à LOW

		# execution de la commande en 4 bits 
		for i in range(0,4) : # les 4 bits de poids fort
			
			# met la broche dans l'état voulu
			if cmdBin[i]=="1": digitalWrite(self.dataPin[i], HIGH) 
			else:digitalWrite(self.dataPin[i], LOW)
			
			#print str(self.dataPin[i])+":"+str(cmdBin[i]) # debug
			
		self.pulseEnable() # impulsion Enable de validation 
		
		for i in range(4,8) : # les 4 bits de poids faible
			
			# met la broche dans l'état voulu
			if cmdBin[i]=="1": digitalWrite(self.dataPin[i-4], HIGH) 
			else:digitalWrite(self.dataPin[i-4], LOW)
			
			#print str(self.dataPin[i-4])+":"+str(cmdBin[i]) # debug

		self.pulseEnable() # impulsion Enable de validation 

	def data4Bits(self, cmdIn):
		
		cmdBin=bin(cmdIn)[2:].zfill(8) # convertit la commande en binaire sur 8 chiffres
		#print type(cmdBin)  #debug
		
		print cmdBin # debug
		
		digitalWrite(self.RS,HIGH) # RS à LOW

		# execution de la commande en 4 bits 
		for i in range(0,4) : # les 4 bits de poids fort
			
			# met la broche dans l'état voulu
			if cmdBin[i]=="1": digitalWrite(self.dataPin[i], HIGH) 
			else:digitalWrite(self.dataPin[i], LOW)
			
			#print str(self.dataPin[i])+":"+str(cmdBin[i]) # debug
			
		self.pulseEnable() # impulsion Enable de validation 
		
		for i in range(4,8) : # les 4 bits de poids faible
			
			# met la broche dans l'état voulu
			if cmdBin[i]=="1": digitalWrite(self.dataPin[i-4], HIGH) 
			else:digitalWrite(self.dataPin[i-4], LOW)
			
			#print str(self.dataPin[i-4])+":"+str(cmdBin[i]) # debug

		self.pulseEnable() # impulsion Enable de validation 
		
	def pulseEnable(self): # impulsion Enable de validation 
		digitalWrite(self.E,LOW) # Enable à LOW
		#delayMicroseconds(1)
		digitalWrite(self.E,HIGH) # Enable à HIGH
		delayMicroseconds(1)
		digitalWrite(self.E,LOW) # Enable à LOW
		delayMicroseconds(100) # le temps d'utilisation des data / execution commande 
		
	# fonctions d'écriture 
	#def write(self, charIn): # affiche le caractere ascii correspondant
	#	self.data4Bits(charIn) 
		
	def write(self, chaineIn): # affiche la chaîne recue
		
		chaine=str(chaineIn)
		
		for c in chaine:
			#print c # debug
			#print ord(c) # debug 
			#print type(ord(c))  debug
			self.data4Bits(ord(c)) # affiche l'ascii correspondant - attention envoyer sous forme d'un str
	
	# gestion ecran 
	def clear(self):
		self.cmd4Bits(LCD_CLEARDISPLAY)
		delay(10) # pour éviter problème
		
	def noDisplay(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay&~LCD_DISPLAYON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)

	def display(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay|LCD_DISPLAYON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
	
	def noCursor(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay&~LCD_CURSORON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
	
	def cursor(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay|LCD_CURSORON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
	
	def noBlink(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay&~LCD_BLINKON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
	
	def blink(self):
		#print bin(self.configDisplay) # debug 
		self.configDisplay=self.configDisplay|LCD_BLINKON# modifie flag display en se basant sur flag ON ... 
		#print bin(self.configDisplay) # debug
		self.cmd4Bits(LCD_DISPLAYCONTROL|self.configDisplay)
	
	def home(self):
		self.cmd4Bits(LCD_RETURNHOME)
		
	
	def setCursor(self, colonneIn, ligneIn): 
		
		debutLignes=[0x00, 0x40, 0x14, 0x54]
		
		if ligneIn>self.nombreLignes:  # pour éviter dépassement
			ligneIn=self.nombreLignes-1
		
		print bin(LCD_SETDDRAMADDR | (colonneIn + debutLignes[ligneIn]))
		self.cmd4Bits(LCD_SETDDRAMADDR | (colonneIn + debutLignes[ligneIn])) # se positionne
		
	def locate(self,ligneIn, colonneIn):# position au format ligne,colonne avec 1,1 pour 1er caractère
		self.setCursor(colonneIn-1, ligneIn-1) 
	
	# config fonctionnement du LCD
	def autoscroll(self):
		self.configEntryMode=self.configEntryMode|LCD_ENTRYSHIFTINCREMENT
		self.cmd4Bits(LCD_ENTRYMODESET|self.configEntryMode)
	
	def noAutoscroll(self):
		self.configEntryMode=self.configEntryMode&~LCD_ENTRYSHIFTINCREMENT
		self.cmd4Bits(LCD_ENTRYMODESET|self.configEntryMode)
		
	def leftToRight(self):
		self.configEntryMode=self.configEntryMode|LCD_ENTRYLEFT
		self.cmd4Bits(LCD_ENTRYMODESET|self.configEntryMode)
	
	def rightToLeft(self):
		self.configEntryMode=self.configEntryMode&~LCD_ENTRYLEFT
		self.cmd4Bits(LCD_ENTRYMODESET|self.configEntryMode)
	
	def scrollDisplayLeft(self):
		self.cmd4Bits(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)
		
	def scrollDisplayRight(self):
		self.cmd4Bits(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)
	


############ fin classe LiquidCrystal ###############


############ Classe Servo #################

freqBasePWM=126 # freq PWM de base utilisée 

# classe Servo pour Pyduino par X. HINAULT - GPLv3 - Nov 2013
class Servo():
	
	def __init__(self):
		self.pin=None
		self.attachedFlag=False
		self.currentAngle=None # angle courant
		self.impulsMin=550
		self.impulsMax=2350
		self.pwmMin=int((255*self.impulsMin/(1000000.0/freqBasePWM) )+0.5)#255*impulsMin/T
		self.pwmMax=int((255*self.impulsMax/(1000000.0/freqBasePWM) )+0.5)
		
		print self.pwmMin # debug
		print self.pwmMax # debug
		
		# RAZ PWM par défaut 
		for pin in PWM:
			setFrequencyPWM(pin, 520) # 126 utilisable avec PWM0, 3, 4, 5  
			analogWrite(pin,0)
			delay(10)
		
	def attach(self, *args):
		#servo.attach(broche)
		#servo.attach(broche, impuls_min, impuls_max)
		
		if len(args)==1: # si forme attach(broche)
			brocheIn=args[0]
			impulsMinIn=self.impulsMin
			impulsMaxIn=self.impulsMax
		else :
			brocheIn=args[0]
			impulsMinIn=args[1]
			impulsMaxIn=args[2]
		
		#print PWM  debug
		print brocheIn
		
		if brocheIn in [PWM0, PWM3, PWM4, PWM5] :
			setFrequencyPWM(brocheIn, freqBasePWM) # freq 126Hz utilisable avec PWM0, 3, 4, 5  
			
			self.pin=brocheIn  # memorise broche 
			self.attachedFlag=True # met flag à True 
			
			self.impulsMin=impulsMinIn
			self.impulsMax=impulsMaxIn
			
			self.pwmMin=int((255*self.impulsMin/(1000000.0/freqBasePWM) )+0.5)#255*impulsMin/T
			self.pwmMax=int((255*self.impulsMax/(1000000.0/freqBasePWM) )+0.5)
			
			#self.pwmMin <=> angle 0°
			#self.pwmMax <=> angle 180°
			
			print self.pwmMin # debug
			print self.pwmMax # debug
			
		else:  # si la broche n'est pas autorisée 
			print "Use pin among PWM0, PWM3, PWM4, PWM5"
		
	
	def write(self, angleDegIn):
		
		angleDegIn=constrain(angleDegIn,0,180)  # limite valeur angle 
		print angleDegIn # debug 
		
		#self.pwmMin <=> angle 0°
		#self.pwmMax <=> angle 180°
		
		impulsPWM=int(rescale(angleDegIn,0,180, self.pwmMin, self.pwmMax))
		print impulsPWM # debug	
		
		print self.pin 
		analogWrite (3, impulsPWM) 
		
		self.currentAngle=angleDegIn

	def writeMicroseconds(self,impulsIn):
		
		impulsPWM=int((255*impulsIn/(1000000.0/freqBasePWM) )+0.5)#255*impulsMin/T
		print impulsPWM # debug
		
		analogWrite(self.pin, impulsPWM)
		
	
	def read(self):
		return  self.currentAngle
	
	def attached(self):
		return  self.attachedFlag
	
	def detach(self) :
		setFrequencyPWM(self.pin, 520) # Frequence par défaut - broche mise à 0 auto 
		analogWrite(self.pin,0) # met la broche à 0 
		self.attachedFlag=False # met flag à True 

############ Fin de la classe Servo #################
