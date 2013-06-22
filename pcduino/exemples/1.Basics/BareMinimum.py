#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# voir : https://github.com/sensor56/pyDuino

# code minimal

from arduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
	return # si vide

# -- fin setup -- 

# -- loop -- 
def loop():
	return # si vide

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while(1): loop() # appelle fonction loop sans fin
