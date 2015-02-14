#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - nov 2012 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# import utiles
import os

# déclarations utiles 

HIGH = 1
LOW  = 0

DEC = 10
BIN = 2
HEX = 16
OCT = 8

# constantes utiles pyDuino
noLoop = False # pour stopper loop
debug  = False # pour message debug
# print "init debug" # message debug de debug... 

READ   = "r"
WRITE  = "w"
APPEND = "a"

# pour uart
UART     = "3"
RX       = 0
TX       = 1
Uart     = None 
uartPort = None # objet global 

# objets internes utiles 
Serial   = None 
Ethernet = None

### chemin de reference ###
#user_name=getpass.getuser()
home_dir = os.getenv("HOME") + "/" # chemin de référence
main_dir = os.getenv("HOME") + "/" # chemin de référence

# constantes de SELECTION
TEXT  = 'TEXT'
IMAGE = 'IMAGE'
AUDIO = 'AUDIO'
VIDEO = 'VIDEO'

### chemins data fichiers texte, sons, image, video ###

data_dir_text  = "data/text/" # data texte relatif a main dir
data_dir_audio = "data/audio/" # data audio
data_dir_image = "data/images/" # data images
data_dir_video = "data/videos/" # data video

#---- chemins sources fichiers texte, sons, images, video
src_dir_text  = "sources/text/" # sources texte relatif a main dir
src_dir_audio = "sources/audio/" # sources audio
src_dir_image = "sources/images/" # sources images
src_dir_video = "sources/videos/" # sources video

# variables globales utiles - non initialisées ici 
# important : pour réaffecter la valeur d'une variable partagée = IL FAUT UTILISER LE NOM DU MODULE DE PARTAGE dans les modules les uutilisant
# sinon c'est une variable globale module qui est créée, pas une variable partagée... 

PLATFORM = None

# fichiers broches E/S
pathMode  = None
pathState = None

# constantes Arduino like
INPUT  = None
OUTPUT = None
PULLUP = None

# identifiants hardware E/S
A0, A1, A2, A3, A4, A5 = None, None, None, None, None, None
PWM = None
PWM0, PWM1, PWM2, PWM3, PWM4, PWM5 = None, None, None, None, None, None

# variables internes utiles 
micros0Syst = 0
millis0Syst = 0