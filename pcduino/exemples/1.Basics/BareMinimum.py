#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDUino - par X. HINAULT - www.mon-club-elec.fr
# voir : https://github.com/sensor56/pyDuino

# code minimal

from arduino import * # importe les fonctions Arduino pour Python

# entete declarative

#--- setup --- 
def setup():
  return 

# -- fin setup -- 

# -- loop -- 
def loop():
	return

# -- fin loop --

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while(1): loop() # appelle fonction loop sans fin
