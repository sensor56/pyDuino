#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# l'appui sur BP inverse LED

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup ---
LEDpin = 5 # LED sur la broche 5
switchPin = 10 # bouton poussoir sur la broche 10, connecté au 0V (la masse)

running = False # déclaration d'une variable de type binaire appelée running et initialisée à false

def setup() :
        pinMode(LEDpin, OUTPUT); // met la broche en sortie
        pinMode(switchPin, PULLUP); // met la broche en entrée avec rappel au plus actif

def loop():
        if digitalRead(switchPin) == LOW : #si le bouton poussoir est appuyé la broche passe à 0V - sinon la broche est à 5V par le rappel au +
                delay(100) # pause anti rebond
                running = not running # inverse la variable binaire
                digitalWrite(LEDpin, running)  # met la LED dans le même état que la variable binaire

#--- obligatoire pour lancement du code --
if __name__=="__main__": # pour rendre le code executable
        setup() # appelle la fonction setup
        while(1): loop() # appelle fonction loop sans fin
