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

L'editeur conseille pour l'edition des codes Pyduino est Geany
A installer dans un Terminal avec la commande
$ sudo apt-get install geany

Ce fichier est la version 0.1.20130706 pour le pcDuino
"""
# message d'accueil 
print "Pyduino for PC Desktop with Arduino - v0.3 - by www.mon-club-elec.fr - 2013 "

# modules utiles 

#-- temps --
import time
import datetime # gestion date 

from threading import Timer # importe l'objet Timer du module threading

#-- math -- 
# import math
from math import *  # pour acces direct aux fonctions math..
import random as rd # pour fonctions aléatoires - alias pour éviter problème avec fonction arduino random()

#-- pour PWM - accès kernel + transposition C to Python -- 
#import fcntl # module pour fonction ioctl
#from ctypes import *
#import ctypes # module pour types C en Python 

#-- système -- 
import subprocess
#import getpass # pour connaitre utilisateur systeme 
import os  # gestion des chemins

import re # expression regulieres pour analyse de chaines

# serie 
try:
	import serial
except: 
	print "ATTENTION : Module Serial manquant : installer le paquet python-serial "

# reseau 
import socket 
import smtplib # serveur mail 

# -- declarations --
# NB : les variables déclarées ici ne sont pas modifiables en dehors du module
# pour modifier la valeur d'une variable de ce module, la seule solution est de la réaffecter dans le programme 
# par exemple noLoop


# constantes Arduino like
INPUT="0"
OUTPUT="1"
PULLUP="8"

# pour uart
#UART="3"
#RX=0
#TX=1

HIGH = 1
LOW =  0

A0, A1, A2, A3, A4,A5 =0,1,2,3,4,5 # identifiant broches analogiques
PWM0, PWM1, PWM2, PWM3, PWM4,PWM5 =3,5,6,9,10,11 # identifiant broches PWM

DEC=10
BIN=2
HEX=16
OCT=8

# constantes utiles pyDuino
noLoop=False # pour stopper loop
debug=False # pour message debug

#--- chemin de reference --- 
#user_name=getpass.getuser()
home_dir=os.getenv("HOME")+"/"  # chemin de référence
main_dir=os.getenv("HOME")+"/"  # chemin de référence

# constantes de SELECTION 
TEXT='TEXT'
IMAGE='IMAGE'
AUDIO='AUDIO'
VIDEO='VIDEO'

#---- chemins data fichiers texte, sons, image, video

data_dir_text="data/text/" # data texte relatif a main dir
data_dir_audio="data/audio/" # data audio 
data_dir_image="data/images/" # data images
data_dir_video="data/videos/" # data video

#---- chemins sources fichiers texte, sons, images, video
src_dir_text="sources/text/" # sources texte relatif a main dir
src_dir_audio="sources/audio/" # sources audio 
src_dir_image="sources/images/" # sources images
src_dir_video="sources/videos/" # sources video


#==== diverses classes utiles utilisées par les fonctions Pyduino ===


# ==================== Fonctions spécifiques pour une plateforme donnée =============================
# =====================>>>>>>>>>> version PC desktop avec Arduino  <<<<<<<<<<< =======================================

# ---- gestion broches E/S numériques ---

# pinMode 
def pinMode(pin, mode):
	
	
	
	if mode==OUTPUT : 
		Uart.println("pinMode("+str(pin)+",1)") # envoi commande - attention OUTPUT c'est 1
		
		out=None
		while not out : # attend reponse 
			out=Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode==INPUT : 
		out=None
		while not out : # tant que pas de reponse envoie une requete
			Uart.println("pinMode("+str(pin)+",0)") # attention input c'est 0
			#print ("pinMode("+str(pin)+",0)") # debug 
			
			out=Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
	elif mode==PULLUP : 
		Uart.println("pinMode("+str(pin)+",0)") # attention INPUT c'est 0
		delay(100) # laisse temps reponse arriver
		print "pinMode("+str(pin)+",0)"
		
		out=None
		while not out : # attend reponse
			out=Uart.waitingAll() # lit les caracteres
		
		print out # debug
		
		digitalWrite(pin,HIGH) # activation du pullup 
	
# digitalWrite 
def digitalWrite(pin, state):
	
	
	Uart.println("digitalWrite("+str(pin)+","+str(state)+")") # 
	#print ("digitalWrite("+str(pin)+","+str(state)+")") # debug

# digitalRead
def digitalRead(pin):
	
	
	# envoi de la commande
	Uart.println("digitalRead("+str(pin)+")") 
	print ("digitalRead("+str(pin)+")")
	# attend un reponse
	out=None
	while not out : # tant que pas de reponse envoie une requete
		out=Uart.waiting() # lit les caracteres
	
	print out # debug
	#out=out.splitlines()
	
	return out # renvoie la valeur



def toggle(pin): # inverse l'etat de la broche
	
	
	
	if digitalRead(pin)==HIGH:
		digitalWrite(pin,LOW)
		return LOW
	else:
		digitalWrite(pin,HIGH)
		return HIGH

#----- gestion broches analogique -----

# analogRead - entrées analogiques 
def analogRead(pinAnalog):
	
	
	""" # mis en fin de lib' = exécution obligatoire au démarrage 
	# au besoin : initialisation port série 
	global uartPort
	if not uartPort : 
		Uart.begin(115200)
		Uart.waitOK() # attend port serie OK 
	"""
	# envoi la commande
	Uart.println("analogRead("+str(pinAnalog)+")") # 
	
	# attend une réponse 
	out=None
	while not out : # tant que pas de reponse 
		#print ("analogRead("+str(pinAnalog)+")") # debug
		#delay(50) # attend reponse
		out=Uart.waiting() # lit les caracteres
	
	if debug: print out # debug
	
	outlines=out.splitlines() # extrait les lignes... une manière simple de supprimer le fin de ligne
	
	outlines=out.splitlines() # extrait les lignes... une manière simple de supprimer le fin de ligne
	if outlines[0].isdigit() :
		return int(outlines[0]) # renvoie la valeur
	else:
		return(-1)	

# analogReadmV - entrées analogiques - renvoie valeur en millivolts
def analogReadmV(pinAnalog):
	
	mesure=analogRead(pinAnalog)
	mesure=rescale(mesure,0,1023,0,5000)
	
	return mesure



# analogWrite # idem Arduino en 0-255
def analogWrite(pinPWMIn, largeurIn):
	
	Uart.println("analogWrite("+str(pinPWMIn)+","+str(largeurIn)+")") # 
	print ("analogWrite("+str(pinPWMIn)+","+str(largeurIn)+")") # debug 

# analogWritePercent(pinPWMIn, largeurIn)=> rescale 0-100 vers 0-255
def analogWritePercent(pinPWMIn, largeurIn):
	global uartPort
	
	if not uartPort : 
		Uart.begin(115200)

	analogWrite(pinPWMIn,rescale(largeurIn,0,100,0,255))
	

################ Fonctions communes ####################

#-- fonction internes pyduino 
# setDebug : pour activer message debug 
def setDebug( boolIn):
	global debug
	debug=boolIn

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
	

#--- fonction timer() : lance fonction avec intervalle en ms
def timer(delaiIn, fonctionIn):
	Timer(delaiIn/1000.0, fonctionIn).start() # relance le timer


# --- fonctions date - RTC - unixtime 
def year():
	return str(datetime.datetime.now().year)

def month():
	if datetime.datetime.now().month<10:
		return "0"+str(datetime.datetime.now().month) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().month)

def day():
	if datetime.datetime.now().day<10:
		return "0"+str(datetime.datetime.now().day) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().day)

def dayOfWeek():
	return str(datetime.datetime.now().weekday()+1)
	# lundi = 1... Dim=7

def hour():
	if datetime.datetime.now().hour<10:
		return "0"+str(datetime.datetime.now().hour) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().hour)

def minute():
	if datetime.datetime.now().minute<10:
		return "0"+str(datetime.datetime.now().minute) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().minute)

def second():
	if datetime.datetime.now().second<10:
		return "0"+str(datetime.datetime.now().second) # ajoute 0 si < 10
	else:
		return str(datetime.datetime.now().second)

def unixtime():
	return str(int(time.time()))

# -- formes mixees --

def nowtime(*arg):
	if len(arg)==0:
		return hour()+minute()+second()  # sans separateur
	elif len(arg)==1:
		sep=str(arg[0])
		return hour()+sep+minute()+sep+second() # avec separateur

def today(*arg):
	if len(arg)==0:
		return day()+month()+year() # sans séparateur
	elif len(arg)==1:
		sep=str(arg[0])
		return day()+sep+month()+sep+year()
	elif len(arg)==2:
		if arg[1]==-1: # forme inversee
			sep=str(arg[0])
			return year()+sep+month()+sep+day()
	
def nowdatetime():
	return today("/") + " " + nowtime(":")
	

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
	# Renvoie une valeur aléatoire entiere
	
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

#============ Système : ligne de commande ======================

def executeCmd(cmd):
	# execute la ligne de commande systeme passee en parametre
	# sans attendre la fin de l'execution 
	
	#p=subprocess.Popen(cmd, shell=True) # exécute la commande et continue 
	p=subprocess.Popen("exec "+ cmd, shell=True) # exécute la commande et continue - exec pour processus renvoyé sinon c'est le shell... 
	# la sortie standard et la sortie erreur ne sont pas interceptées donc s'affieront dans le Terminal mais non accessible depuis le code..
	
	return(p)


def executeCmdWait(cmd):
	# execute la ligne de commande systeme passee en parametre
	# et attend la fin de l'execution 
	#subprocess.Popen(cmd, shell=False).wait
	# subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait # attention - wait attend pas si SHell=True !

	# en cas de commande : cmd -params "chaine"
	subcmd=cmd.split("\"") # pour extraire chaîne avant pour pas appliquer séparation par espace sur la chaîne
	#print subcmd
	subsubcmd=subcmd[0].split(" ") # pour avoir format liste [ arge, arg, arg] attendu par check_call - pose probleme si chaine en param
	#print subsubcmd  #debug
	try:
		subsubcmd.remove('') # enleve '' car bloque commande si present... sinon provoque erreur d'ou try except
	except:
		pass
	
	#print subsubcmd  #debug
	
	if len(subcmd)==1: # si pas de chaine 
		subprocess.check_call(subsubcmd)
	elif len(subcmd)>1: 
		subsubcmd.append("\"" + str(subcmd[1] )+"\"") # ajoute la chaine en + encadree par " "
		#print (" \" " + str(subcmd[1] )+"\"") # debug
		#print subsubcmd # debug
		subprocess.check_call(subsubcmd ) 


def executeCmdOutput(cmd):
	# execute la ligne de commande systeme passee en parametre
	# capture la sortie console et attend la fin de l'execution 
	
	pipe=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout # execute la commande 
	out=pipe.read() # lit la sortie console
	pipe.close() # ferme la sortie console
	
	return(out)
	

########################## fichiers et data texte ###############################

##------ gestion fichier et répertoires -------

# les variables de chemin et leur valeur par defaut :
#--- chemin de reference --- 
#home_dir=os.getenv("HOME")+"/"  # chemin de référence
#main_dir=os.getenv("HOME")+"/"  # chemin de référence

#---- chemins data fichiers texte, sons, image, video
#data_dir_text="data/text/" # data texte relatif a main dir
#data_dir_audio="data/audio/" # data audio 
#data_dir_image="data/images/" # data images
#data_dir_video="data/videos/" # data video

#---- chemins sources fichiers texte, sons, images, video
#src_dir_text="sources/text/" # sources texte relatif a main dir
#src_dir_audio="sources/audio/" # sources audio 
#src_dir_image="sources/images/" # sources images
#src_dir_video="sources/videos/" # sources video

def homePath():
	return os.getenv("HOME")+"/"

def mainPath():
	return main_dir

def setMainPath(pathIn):
	global main_dir
	main_dir=pathIn

#-- (get) data Path 
def dataPath(typeIn):
	if typeIn==TEXT:
		return data_dir_text
	elif typeIn==IMAGE:
		return data_dir_image
	elif typeIn==AUDIO:
		return data_dir_audio
	elif typeIn==VIDEO:
		return data_dir_video
	else: 
		print "Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO"

#--- set data Path
def setDataPath(typeIn, dirIn):
	if typeIn==TEXT:
		global data_dir_text
		data_dir_text=dirIn
	elif typeIn==IMAGE:
		global data_dir_image
		data_dir_image=dirIn
	elif typeIn==AUDIO:
		global data_dir_audio
		data_dir_audio=dirIn
	elif typeIn==VIDEO:
		global data_dir_video
		data_dir_video=dirIn
	else: 
		print "Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO"

#-- (get) source Path 
def sourcesPath(typeIn):
	if typeIn==TEXT:
		return src_dir_text
	elif typeIn==IMAGE:
		return src_dir_image
	elif typeIn==AUDIO:
		return src_dir_audio
	elif typeIn==VIDEO:
		return src_dir_video
	else: 
		print "Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO"

#--- set sources Path
def setSourcesPath(typeIn, dirIn):
	if typeIn==TEXT:
		global src_dir_text
		src_dir_text=dirIn
	elif typeIn==IMAGE:
		global src_dir_image
		src_dir_image=dirIn
	elif typeIn==AUDIO:
		global src_dir_audio
		src_dir_audio=dirIn
	elif typeIn==VIDEO:
		global src_dir_video
		src_dir_video=dirIn
	else: 
		print "Erreur : choisir parmi TEXT, IMAGE, AUDIO, VIDEO"


#-- fonction gestion répertoires / fichiers 

def exists(filepathIn): # teste si le chemin ou fichier existe
	"""try:
		with open(filepathIn): return True
	except IOError:
		#print "Le fichier n'existe pas" # debug
		return False
	"""
	if os.path.isfile(filepathIn) or os.path.isdir(filepathIn):
		return True
	else :
		return False

def isdir(pathIn):
	return os.path.isdir(pathIn)
	

def isfile(filepathIn):
	return os.path.isfile(filepathIn)

def dirname(pathIn):
	return os.path.dirname(pathIn)+"/"
	

def currentdir():
	return os.getcwd()+"/"

def changedir(pathIn):
	os.chdir(pathIn)

def rewindDirectory():
	os.chdir("..")  # remonte d'un niveau

def mkdir(pathIn): # crée le répertoire si il n'existe pas
	# os.mkdir(pathIn) ne créée pas les rep intermediaires
	try:
		os.makedirs(pathIn) # cree les rep intermediaires
		return True
	except OSError:
		print("Probleme creation")
		return False

def rmdir(pathIn): # efface le répertoire
	try:
		os.rmdir(pathIn)  #efface repertoire
		return True
	except OSError:
		print "Effacement impossible"
		return False

def listdirs(pathIn): # liste les repertoires 
	if exists(pathIn):
		onlydirs = [ f for f in os.listdir(pathIn) if os.path.isdir(os.path.join(pathIn,f)) ]
		return sorted(onlydirs)
	else: 
		return False

def listfiles(pathIn): # liste les fichiers 
	if exists(pathIn):
		onlyfiles = [ f for f in os.listdir(pathIn) if os.path.isfile(os.path.join(pathIn,f)) ]
		# voir : http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
		return sorted(onlyfiles)
	else: 
		return False

def dircontent(pathIn): # liste rep suivi des fichiers
	if exists(pathIn):
		out=""
		for dirname in listdirs(pathIn): # les rép
			out=out+dirname+"/\n"
		
		for filename in listfiles(pathIn):   # les fichiers
			out=out+filename+"\n"
		
		return out 
	else: 
		return False


# open (path, mode) avec mode parmi r, w ou a -- fonction native Python --> renvoie un objet file 

def remove(filepathIn):
	try:
		os.remove(filepathIn)  #efface fichier
		return True
	except OSError:
		print "Effacement impossible"
		return False

#---- fonctions objet file ----- 

# voir http://docs.python.org/2/library/stdtypes.html#bltin-file-objects 

# close () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.close

# flush () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.flush

# name() -- Python --> http://docs.python.org/2/library/stdtypes.html#file.name

# tell () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.tell

# seek () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.seek

# size () -- Python --> 
def size(filepathIn):
	return os.path.getsize(filepathIn)

# read () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.read

# write () -- Python --> http://docs.python.org/2/library/stdtypes.html#file.write 

# readLine() -- Python --> http://docs.python.org/2/library/stdtypes.html#file.readline

# readLines() -- Python --> http://docs.python.org/2/library/stdtypes.html#file.readlines

#-- fonctions Pyduino utiles files --- 

def appendDataLine(filepathIn, dataIn):
	if exists(filepathIn):
		dataFile=open(filepathIn,'a') # ouvre pour ajout donnees
		dataFile.write(str(dataIn)+"\n")
		dataFile.close()
	elif not exists(filepathIn):
		dataFile=open(filepathIn,'w') # cree fichier pour ajout donnees
		dataFile.write(str(dataIn)+"\n")
		dataFile.close()


############################ Reseau ##################################

def httpResponse(): # reponse HTTP par defaut
	return """
HTTP/1.0 200 OK
Content-Type: text/html
Connnection: close

""" # ligne vide finale obligatoire ++ 

# classe Ethernet - emule classe acces au materiel réseau 
class Ethernet():
	# def __init__(self): # constructeur principal
	
	def localIP(self):
		# return socket.gethostbyname(socket.gethostname()) ne fonctionne pas... 
		
		sortieConsole=executeCmdOutput("ifconfig") # execute commande et attend 5s
		#print sortieConsole - debug
		
		#result=re.findall(r'^.*inet  adr:(.*\..*\..*\..*) .*$',sortieConsole, re.M) # extrait *.*.*.* de la chaine au format inet adr: *.*.*.* si la chaine est au format valide  + tolerant fin chaine  
		result=re.findall(r'^.*inet addr:(.*\..*\..*\..*)  B.*$', sortieConsole, re.M)
		#print result
		if len(result)>0 :return result[0]
		else: return

class EthernetServer(socket.socket) : # attention recoit classe du module, pas le module !

	def __init__(self,ipIn, portIn): # constructeur principal
		#self=socket.socket( socket.AF_INET,socket.SOCK_STREAM) # self est un objet serveur
		#self.bind((ipIn,portIn)) # lie l'adresse et port au serveur # '' pour interface disponible 
		
		super(EthernetServer, self).__init__(socket.AF_INET,socket.SOCK_STREAM) # initialise Ethernet class en tant que socket...
		
		# a present self dispose de toutes les fonctions socket ! 
		#print type(self) # debug
		#print dir(self) # debug
		
		#self.socket(socket.AF_INET,socket.SOCK_STREAM)
		#self.socket( AF_INET,SOCK_STREAM)  # socket.socket( AF_INET,SOCK_STREAM)    # socket.socket([family[, type[, proto]]])
		
		self.bind((ipIn,portIn)) # lie l'adresse et port au serveur # '' pour interface disponible 
		
	
	
	def begin(self, *arg):
		
		
		if len(arg)==0: # si pas de nombre client precise
			self.listen(5) # fixe a 5 
		elif len(arg)==1: # si nombre client
			self.listen(arg[0]) # fixe au nombre voulu
	
	def clientAvailable(self):
		client,adresseDistante=self.accept() # attend client entrant
		return client, adresseDistante[0]
		# l'adresse recue est un tuple - ip est le 1er element

	def readDataFrom(self, clientDistantIn, *arg):
		
		# arg = rien ou maxIn
		if len(arg)==0:
			maxIn=1024
		elif len(arg)==1:
			maxIn=arg[0]
		
		chaineRecue=clientDistantIn.recv(maxIn)#.strip() 
		chaineRecue.decode('utf-8')
		return chaineRecue
	
	def writeDataTo(self, clientDistantIn, reponseIn):
		clientDistantIn.send(reponseIn) # préférer sendAll ? 
"""
class EthernetClient(socket.socket) : # attention recoit classe du module, pas le module !
	
	def read():
		#--- requete client ---
		rec=self.recv(1024).strip()
		rec.decode('utf-8')
		print rec
"""
# close() -- module socket -- classe socket -- Python --> http://docs.python.org/2/library/socket.html#socket.socket.close


# classe MailServer

class MailServer():
	
	def __init__(self):
		self.name=""
		self.port=0
		self.fromMail=""
		self.fromPassword=""
		self.toMail=""
		
		self.subject=""
		self.msg=""
		self.imageToJoin=""
	
	def setName(self,nameIn):
		self.name=nameIn
	
	def setPort(self,portIn):
		self.port=portIn
		
	def setFromMail(self,fromMailIn):
		self.fromMail=fromMailIn
		
	def setFromPassword(self,fromPasswordIn):
		self.fromPassword=fromPasswordIn
		
	def setToMail(self,toMailIn):
		self.toMail=toMailIn
		
	def setSubject(self,subjectIn):
		self.subject=subjectIn
	
	def setMsg(self,msgIn):
		self.msg=msgIn
	
	def setImageToJoin(self,pathIn):
		self.imageToJoin=pathIn
	
	def getHeader(self):
		#header
		header='To:' + self.toMail + '\n'
		header=header+ 'From:' + self.fromMail +'\n'
		header=header + 'Subject:' + self.subject + '\n'
		return header
		
	def sendMail(self):
		
		from email.mime.text import MIMEText
		
		# connexion serveur smtp
		smtpserver=smtplib.SMTP(self.name, self.port)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		print smtpserver.login(self.fromMail, self.fromPassword)
		
		"""
		# preparation du mail 
		mail=self.getHeader()+self.msg+"\n\n"
		print mail # debug
		"""
		
		# preparation du mail - utilise module email
		mail = MIMEText(self.msg)
		mail['Subject'] = self.subject
		mail['From'] = self.fromMail
		mail['To'] = self.toMail
		print ""
		print mail.as_string() # debug
		
		# envoi du mail 
		smtpserver.sendmail(self.fromMail, [self.toMail], mail.as_string())
		
		# fermeture serveur smtp
		#smtpserver.close()
		print smtpserver.quit()
	
	def sendMailImage(self):
		
		from email.mime.text import MIMEText
		from email.mime.image import MIMEImage
		from email.mime.multipart import MIMEMultipart
		
		# connexion serveur smtp
		smtpserver=smtplib.SMTP(self.name, self.port)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(self.fromMail, self.fromPassword)
		
		"""
		# preparation du mail 
		mail=self.getHeader()+self.msg+"\n\n"
		print mail # debug
		"""
		
		# preparation du mail - utilise module email
		#mail = MIMEText(self.msg)
		mail=MIMEMultipart()
		mail['Subject'] = self.subject
		mail['From'] = self.fromMail
		mail['To'] = self.toMail
		mail.preamble = self.subject
		
		msg = MIMEText(self.msg) # le texte
		mail.attach(msg) # attache le texte au mail
		
		fp=open(self.imageToJoin,'rb') # ouvre fichier image en lecture binaire
		img=img = MIMEImage(fp.read()) # lit le fichier et récupere l'objet image obtenu
		fp.close()# ferme le fichier
		
		mail.attach(img) # attache l'image au mail
		
		print mail.as_string() # debug
		
		# envoi du mail 
		smtpserver.sendmail(self.fromMail, [self.toMail], mail.as_string())
		
		# fermeture serveur smtp
		#smtpserver.close()
		smtpserver.quit()


#------ fin serveur mail --- 

# classe Uart pour communication série UART 

uartPort=None # objet global 

class Uart():
	
	# def __init__(self): # constructeur principal
	
	
	def begin(self,rateIn, *arg): # fonction pour émulation de begin... Ne fait rien... 
		
		global uartPort
		
		# configure pin 0 et 1 pour UART (mode = 3)
		#pinMode(RX,UART) - sur le pcduino
		#pinMode(TX,UART)
		
		#-- initialisation port serie uart 
		try:
			if len(arg)==0: # si pas d'arguments
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 10) # initialisation port serie uart
				#uartPort=serial.Serial('/dev/ttyACM0', rateIn, timeout = 10) # initialisation port serie uart
				uartPort=serial.Serial('/dev/ttyACM0', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 10)
				uartPort.flushInput() # vide la file d'attente série
			if len(arg)==1 : # si timeout
				#uartPort=serial.Serial('/dev/ttyS1', rateIn, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = arg[0]) # initialisation port serie uart
				uartPort=serial.Serial('/dev/ttyACM0', rateIn, timeout = arg[0]) # initialisation port serie uart
				uartPort.flushInput() # vide la file d'attente série
				
			print("Initialisation Port Serie : /dev/ttyACM0 @ " + str(rateIn) +" = OK ") # affiche debug
			
		except:
			print ("Erreur lors initialisation port Serie") 
			
	def waitOK(self): # fonction pour attendre reponse OK suite initialisation
		out=None
		while not out : # attend une réponse 
			out=Uart.waitingAll() # lit tous les caracteres
		
		print out
	
	
	def println(self,text, *arg):  # message avec saut de ligne
		# Envoi chaine sur port serie uart 
		# Supporte formatage chaine façon Arduino avec DEC, BIN, OCT, HEX
		
		global uartPort
		
		# attention : arg est reçu sous la forme d'une liste, meme si 1 seul !
		text=str(text) # au cas où
		
		arg=list(arg) # conversion en list... évite problèmes.. 
		
		#print arg - debug
		
		if not len(arg)==0: # si arg a au moins 1 element (nb : None renvoie True.. car arg existe..)
			if arg[0]==DEC and text.isdigit():
				# print(text)
				out=text
			elif arg[0]==BIN and text.isdigit():
				out=bin(int(text))
				# print(out)
			elif arg[0]==OCT and text.isdigit():
				out=oct(int(text))
				# print(out)
			elif arg[0]==HEX and text.isdigit():
				out=hex(int(text))
				# print(out)
		else: # si pas de formatage de chaine = affiche tel que 
			out=text
			# print(out)
		
		uartPort.write(out+chr(10)) # + saut de ligne 
		#print "Envoi sur le port serie Uart : " + out+chr(10) # debug
		
		# ajouter formatage Hexa, Bin.. cf fonction native bin... 
		# si type est long ou int
	"""
	def print(self,text): # affiche message sans saut de ligne
		
		#text=str(txt)
		
		print(text), # avec virgule pour affichage sans saus de ligne
	"""
	
	def available(self):
		global uartPort
		
		if uartPort.inWaiting() : return True
		else: return False
		
	def flush(self):
		global uartPort
		return uartPort.flush()
	
	def read(self):
		global uartPort
		return uartPort.read()
	
	def write(self, strIn):
		global uartPort
		uartPort.write(strIn)
		
	#--- lecture d'une ligne jusqu'a caractere de fin indique
	def waiting(self, *arg): # lecture d'une chaine en reception sur port serie 
		
		global uartPort
		
		if len(arg)==0: endLine="\n" # par defaut, saut de ligne
		elif len(arg)==1: endLine=arg[0] # sinon utilise caractere voulu
		
		#-- variables de reception -- 
		chaineIn=""
		charIn=""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn=uartPort.read() # on lit le caractere
			#print charIn # debug
			
			if charIn==endLine: # si caractere fin ligne , on sort du while
				#print("caractere fin de ligne recu") # debug
				break # sort du while
			else: #tant que c'est pas le saut de ligne, on l'ajoute a la chaine 
				chaineIn=chaineIn+charIn
				# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine
	
	#--- lecture de tout ce qui arrive en réception 
	def waitingAll(self): # lecture de tout en reception sur port serie 
		
		global uartPort
		
		#-- variables de reception -- 
		chaineIn=""
		charIn=""
		
		#delay(20) # laisse temps aux caracteres d'arriver
		
		while uartPort.inWaiting(): # tant que au moins un caractere en reception
			charIn=uartPort.read() # on lit le caractere
			#print charIn # debug
			chaineIn=chaineIn+charIn
			# print chaineIn # debug
			
		#-- une fois sorti du while : on se retrouve ici - attention indentation 
		if len(chaineIn)>0: # ... pour ne pas avoir d'affichage si ""	
			#print(chaineIn) # affiche la chaine # debug
			return chaineIn  # renvoie la chaine 
		else:
			return False # si pas de chaine


# fin classe Uart

########################## FONCTIONS MULTIMEDIA ################################

#================= IMAGE ==========================

# constante brg pour couleur police

blue=(255,0,0)
red=(0,0,255)
green=(0,255,0)
yellow=(0,255,255)

#--- creation d'un buffer principal RGB utilise par les fonctions 
Buffer=None # déclare buffer principal non initialisé
webcam=None # declare webcam - non initialise 
iplImgSrc=None # declare objet pour capture image

def initWebcam(*arg):
	# arg : indexIn, widthIn, heightIn
	
	# prise en compte des parametres 
	if len(arg)==3:
		indexCam=arg[0]
		widthCam=arg[1]
		heightCam=arg[2]
	else:
		indexCam=0
		widthCam=320
		heightCam=240
	
	print ("Parametres capture image : index cam = " + str(indexCam) 
	+ " | " + str (widthCam) + "x" + str(heightCam))
	
	#-- initialisation de la camera
	#indexCam=0 # index de la webcam a utiliser - voir ls /dev/video* - utiliser -1 si pas d'indice
	global webcam
	webcam=cv.CaptureFromCAM(indexCam) # declare l'objet capture sans designer la camera - remplace CreateCameraCapture
	#print (webcam) # debug

	cv.SetCaptureProperty(webcam,cv.CV_CAP_PROP_FRAME_WIDTH,widthCam) # definit largeur image capture
	cv.SetCaptureProperty(webcam,cv.CV_CAP_PROP_FRAME_HEIGHT,heightCam) # definit hauteur image capture
	
	# creation buffer image taille idem capture
	global Buffer 
	Buffer=cv.CreateImage((widthCam,heightCam), cv.IPL_DEPTH_8U, 3) # buffer principal 3 canaux 8 bits non signes - RGB --
	
	captureAutoLive() # premier appel captureAutoLive
	

# fonction interne pour lecture automatique frames webcam a frequence = ~ fps
def captureAutoLive():
	global webcam, Buffer, iplImgSrc
	
	cv.QueryFrame(webcam) # recupere un IplImage en provenance de la webcam dans le iplImage Source
	
	timer(200, captureAutoLive) # auto appel de la fonction de capture de facon a lire 5 - 6 frame par seconde
	# le but ici est uniquement de lire les frames pour eviter decalage lors captureImage...
	# qui sinon renvoie frame precedent et non derniere capture

def captureImage(*arg):
	# arg : pathImageIn
	
	# gestion des arguments recus
	if len(arg)==0:
		print ("Preciser le chemin d'enregistrement de l'image")
		return
	elif len(arg)>0: # si arguments recus
		filepathImage=arg[0]
		
	#--- capture Image 
	# webcam testee out of the box : Logitech C170
	
	"""
	#-- initialisation de la camera
	#indexCam=0 # index de la webcam a utiliser - voir ls /dev/video* - utiliser -1 si pas d'indice
	webcam=cv.CaptureFromCAM(indexCam) # declare l'objet capture sans designer la camera - remplace CreateCameraCapture
	#print (webcam) # debug
	cv.SetCaptureProperty(webcam,cv.CV_CAP_PROP_FRAME_WIDTH,widthCam) # definit largeur image capture
	cv.SetCaptureProperty(webcam,cv.CV_CAP_PROP_FRAME_HEIGHT,heightCam) # definit hauteur image capture
	
	global Buffer 
	Buffer=cv.CreateImage((widthCam,heightCam), cv.IPL_DEPTH_8U, 3) # buffer principal 3 canaux 8 bits non signes - RGB --
	"""
	global webcam, Buffer, iplImgSrc
	
	"""
	# lire les premieres images pour eviter probleme decalage
	for i in range(7):
		iplImgSrc=cv.QueryFrame(webcam) # recupere un IplImage en provenance de la webcam
	
	iplImgSrc=cv.QueryFrame(webcam) # recupere un IplImage en provenance de la webcam dans le Buffer
	cv.Copy( iplImgSrc,Buffer)# cv.Copy(src, dst, mask=None) -> None
	#Buffer=cv.QueryFrame(webcam)
	"""
	# preferer utilisation fonction capture live auto permettant copier/lire derniere frame a tout moment
	# la derniere frame live est dans iplImgSrc - ici recapturer pour avoir derniere frame... 
	iplImgSrc=cv.QueryFrame(webcam) # recupere un IplImage en provenance de la webcam dans le Buffer
	cv.Copy( iplImgSrc,Buffer)# cv.Copy(src, dst, mask=None) -> None
	
	# une alternative possible à opencv = gstreamer 
	# pipeline : 
	#  gst-launch v4l2src device=/dev/video0 num-buffers=1 ! jpegenc ! filesink location=test.jpg
	

def loadImage(filepathImageIn):
	global Buffer
	Buffer=cv.LoadImage(filepathImageIn, cv.CV_LOAD_IMAGE_COLOR) # charge l'image sous forme d'une iplImage 3 canaux
	

def saveImage(filepathImageIn):
	global Buffer
	cv.SaveImage(filepathImageIn, Buffer)

def showImage(*arg):
	
	
	# filepathIn ou rien 
	
	if len(arg)==0: # si pas de nom de fichier précisé => on utilise un fichier transitoire.. 
		filepathImage=homePath()+"imageTrans.jpg"
		saveImage(filepathImage)
		executeCmd("gpicview " + str(filepathImage)) # affiche image avec viewer lxde = gpicview
	elif len(arg)==1: # si chemin recu 
		filepathIn=arg[0]
		if exists(filepathIn):
			executeCmd("gpicview " + str(filepathIn)) # affiche image avec viewer lxde = gpicview
		else : 
			print ("Fichier image n'existe pas !")

"""
def showImage():
	global Buffer
	cv.NamedWindow("Buffer") #cv.NamedWindow(name, flags=CV_WINDOW_AUTOSIZE) 
	cv.ShowImage("Buffer", Buffer) # cv.ShowImage(name, image) -> None
	# ne fonctionne pas... 
	
"""

def closeImage(): # ferme le visionneur d'image si ouvert 
	# ferme visionneur image 
	try :
		executeCmdWait("killall gpicview") # ferme image precedente 
	except:
		pass
	

def addTextOnImage(textIn, xPosIn, yPosIn, bgrIn, fontScaleIn):
	global Buffer
	# bgr est soit un des identifiants predefinis soit un (b,g,r)
	
	#  initFont(name_font, hscale, vscale, shear=0, thickness=1, line_type=8 ) -> cvFont
	font=cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, fontScaleIn, fontScaleIn, 0, 2, 8) 
	cv.PutText(Buffer, textIn, (xPosIn,yPosIn),font, bgrIn)# cv.PutText(img, text, org, font, color) -> None
	
	
def width(): # renvoie la width (largeur) courante du Buffer image
	global Buffer
	return Buffer.width 
	

def height(): # renvoie le height (hauteur) courante du Buffer image
	global Buffer
	return Buffer.height
	

#================= AUDIO / VOIX ==========================

PICO='pico'
ESPEAK='espeak'

#--------------- Audio -----------------
def playSound(filepathIn):
	#print os.path.dirname(filepathIn) # debug
	if os.path.dirname(filepathIn)=='':
		filepathIn=mainPath()+sourcesPath(AUDIO)+filepathIn # chemin par défaut si nom fichier seul
		
	#print filepathIn  #debug
	executeCmdWait("mplayer -msglevel all=-1 " + filepathIn) # seul message erreur cf 0   fatal messages only
	# voir : http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.txt

def waitSound(*args):
	# ( [seuil], [duree] )
	
	# arg : soit rien, soit duree detect, seuil detect
	if len(args)==0 :
		executeCmdWait("rec -q trans.wav silence 1 0.1 10% trim 0 1") # seuil 10% pendant 0,1sec - enreg 1 sec..
	if len(args)==2:
		executeCmdWait("rec -q trans.wav silence 1 " + str(args[1]) +" "+str(args[0])+"% trim 0 1") # seuil n% pendant nsec - enreg 1 sec..
		# attention seuil = arg[0] et duree =arg[1]


#---------- Voix ------------- 
def speak(textIn, *arg):
	
	
	# arg : soit rien, soit ESPEAK ou PICO
	if len(arg)==0 : # si pas précisé = pico par defaut 
		executeCmdWait("pico2wave -l fr-FR -w " + homePath()+"pico.wav " + "\""+str(textIn)+"\"") # encadre chaine de " "
		executeCmdWait("mplayer -msglevel all=-1 " + homePath()+"pico.wav " )
	elif len(arg)==1 : # sinon, on utilise le moteur tts voulu
		if arg[0]==PICO:
			executeCmdWait("pico2wave -l fr-FR -w " + homePath()+"pico.wav " + "\""+str(textIn)+"\"") # encadre chaine de " "
			executeCmdWait("mplayer -msglevel all=-1 " + homePath()+"pico.wav " )
		elif arg[0]==ESPEAK:
			executeCmdWait("espeak -v fr -s 140 "+"\""+str(textIn)+"\"" )

def recordSound(filepathIn, dureeIn):
	if not exists(os.path.dirname(filepathIn)): # cree le rep si existe pas 
		mkdir(os.path.dirname(filepathIn))
	
	executeCmdWait("arecord -d "+str(dureeIn)+" -r 16000 -f cd "+ str(filepathIn)) # enregistre 5 secondes en qualite CD a 16000hz dans fichier voulu
	
def analyzeVoice(filepathIn):
	
	workdir=os.path.dirname(filepathIn)+"/" # repertoire du fichier son 
	
	# élimine les silences 
	executeCmdWait("sox " + str(filepathIn)+" "+ str(workdir)+"trim.wav silence 1 0.1 1% -1 0.1 1%") # elimine les silences du fichier son
	#print ("sox " + str(filepathIn)+" "+ str(workdir)+"trim.wav silence 1 0.1 1% -1 0.1 1%") # debug
	print ("Effacement des silences")
	
	# test duree après effacement silence
	duration=executeCmdOutput("soxi -D "+ str(workdir)+"trim.wav") # recupere duree fichier
	#print ("soxi -D "+ str(workdir)+"trim.wav") # debug
	print "duree = " + duration
	
	# si duree insuffisante : sortie de la fonction = evite connexion inutile au serveur
	if float(duration)<0.1 :
		print "Duree < 0.1 seconde : pas de connexion au serveur !"
		return "" # renvoi chaine vide 
	
	# si la duree est suffisante : la suite est executee = envoi chaine vers serveur vocal 
	
	# formatage du fichier son pour reconnaissance de voix google en ligne 
	executeCmdWait("sox " + str(filepathIn)+" "+ str(workdir)+"fichier.flac rate 16k") # convertit le fichier *.wav en fichier *.flac avec echantillonage 16000hz
	#print ("sox " + str(filepathIn)+" "+ str(workdir)+"fichier.flac rate 16k") # debug 
	print ("Conversion fichier voix...")
	
	
	out=executeCmdOutput("wget -4 -q -U \"Mozilla/5.0\" --post-file "+ str(workdir)+"fichier.flac"+" --header=\"Content-Type: audio/x-flac; rate=16000\" -O  - \"http://www.google.com/speech-api/v1/recognize?lang=fr&client=chromium\" ")
	#print ("wget -4 -q -U \"Mozilla/5.0\" --post-file "+ str(workdir)+"fichier.flac"+" --header=\"Content-Type: audio/x-flac; rate=16000\" -O  - \"http://www.google.com/speech-api/v1/recognize?lang=fr&client=chromium\" ") # debug
	#print out # debug
	print ("Connexion serveur reconnaissance vocale...")
	
	# extraction de la chaine reconnue au sein de la reponse google voice a l'aide des expressions regulieres
	result=re.findall(r'^.*\[\{.*:"(.*)",".*$', out) # trouve le texte place --[{--:"**"-- au niveau des **
	print (result) # debug
	
	if len(result)>0:result=str(result[0])
	else: result=""
	
	print (result) # debug
	return str(result)
	

#============================ VIDEO ======================================
def playVideo(filepathIn):
	#print os.path.dirname(filepathIn) # debug
	if os.path.dirname(filepathIn)=='':
		filepathIn=mainPath()+sourcesPath(AUDIO)+filepathIn # chemin par défaut si nom fichier seul
		
	#print filepathIn  #debug
	executeCmd("mplayer -msglevel all=-1 -fs " + filepathIn) # seul message erreur cf 0   fatal messages only
	# voir : http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.txt
	# -fs pour fullscreen - sortie avec esc..

def stopVideo():
	# ferme mplayer
	try :
		executeCmdWait("killall mplayer") # ferme mplayer
	except:
		pass
	
#---- classes utiles multimedia --------

# ...

########################## fin multimedia #########################################


########################### --------- initialisation ------------ #################

Serial = Serial() # declare une instance Serial pour acces aux fonctions depuis code principal
Ethernet = Ethernet() # declare instance Ethernet implicite pour acces aux fonctions 
Uart = Uart() # declare instance Uart implicite 

micros0Syst=microsSyst() # mémorise microsSyst au démarrage
millis0Syst=millisSyst() # mémorise millisSyst au démarrage


# initialisation port série dès le début car va communiquer ave Arduino
Uart.begin(115200) # initialise comm' série 
delay(3000) # laisse le temps à la réponse d'arriver
Uart.waitOK() # attend réponse port serie OK 


