#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Tous droits réservés - 2013
# www.mon-club-elec.fr - Licence GPLv3

### imports ###

### multimedia ### 
#from PyQt4.QtGui import *
#from PyQt4.QtCore import * # inclut QTimer..

try:
	from cv2 import * # importe module OpenCV Python - le module cv est un sous module de cv2
except: 
	print "ATTENTION : Module OpenCV manquant : installer le paquet python-opencv "

### expressions regulieres ###
import re # expression regulieres pour analyse de chaines

### importe les autres modules Pyduino ###
from coreCommon import * # variables communes
from coreBase   import *
from coreSystem import *
from coreLibs   import *

### FONCTIONS MULTIMEDIA ###

### IMAGE ###

# constante brg pour couleur police

blue   = (255, 0, 0)
red    = (0, 0, 255)
green  = (0, 255, 0)
yellow = (0, 255, 255)

### creation d'un buffer principal RGB utilise par les fonctions ### 
Buffer    = None # déclare buffer principal non initialisé
webcam    = None # declare webcam - non initialise 
iplImgSrc = None # declare objet pour capture image

def initWebcam(*arg):
	# arg : indexIn, widthIn, heightIn
	
	# prise en compte des parametres 
	if len(arg) == 3:
		indexCam  = arg[0]
		widthCam  = arg[1]
		heightCam = arg[2]
	else:
		indexCam  = 0
		widthCam  = 320
		heightCam = 240
	
	print "Parametres capture image : index cam = " + str(indexCam) + " | " + str (widthCam) + "x" + str(heightCam)
	
	### initialisation de la camera ###
	#indexCam=0 # index de la webcam a utiliser - voir ls /dev/video* - utiliser -1 si pas d'indice
	global webcam
	webcam = cv.CaptureFromCAM(indexCam) # declare l'objet capture sans designer la camera - remplace CreateCameraCapture
	#print (webcam) # debug

	cv.SetCaptureProperty(webcam, cv.CV_CAP_PROP_FRAME_WIDTH, widthCam) # definit largeur image capture
	cv.SetCaptureProperty(webcam, cv.CV_CAP_PROP_FRAME_HEIGHT, heightCam) # definit hauteur image capture
	
	# creation buffer image taille idem capture
	global Buffer 
	Buffer = cv.CreateImage((widthCam,heightCam), cv.IPL_DEPTH_8U, 3) # buffer principal 3 canaux 8 bits non signes - RGB --
	
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
		
	### capture Image ###
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
	iplImgSrc = cv.QueryFrame(webcam) # recupere un IplImage en provenance de la webcam dans le Buffer
	cv.Copy(iplImgSrc,Buffer)# cv.Copy(src, dst, mask=None) -> None
	
	# une alternative possible à opencv = gstreamer 
	# pipeline : 
	#  gst-launch v4l2src device=/dev/video0 num-buffers=1 ! jpegenc ! filesink location=test.jpg
	
	# gestion des arguments recus
	if len(arg) == 0:
		return # sort sans enregistrer si pas de chemin reçu
	elif len(arg) > 0: # si arguments recus
		filepathImage = arg[0]
		saveImage(filepathImage) # on enregistre fichier si chemin recu

def loadImage(filepathImageIn):
	global Buffer
	Buffer = cv.LoadImage(filepathImageIn, cv.CV_LOAD_IMAGE_COLOR) # charge l'image sous forme d'une iplImage 3 canaux
	

def saveImage(filepathImageIn):
	global Buffer
	cv.SaveImage(filepathImageIn, Buffer)

def showImage(*arg):
	# filepathIn ou rien 
	
	if len(arg) == 0: # si pas de nom de fichier précisé => on utilise un fichier transitoire.. 
		filepathImage = homePath() + "imageTrans.jpg"
		saveImage(filepathImage)
		executeCmd("gpicview " + str(filepathImage)) # affiche image avec viewer lxde = gpicview
	elif len(arg) == 1: # si chemin recu 
		filepathIn = arg[0]
		if exists(filepathIn):
			executeCmd("gpicview " + str(filepathIn)) # affiche image avec viewer lxde = gpicview
		else : 
			print "Fichier image n'existe pas !"

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
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, fontScaleIn, fontScaleIn, 0, 2, 8) 
	cv.PutText(Buffer, textIn, (xPosIn,yPosIn),font, bgrIn)# cv.PutText(img, text, org, font, color) -> None
	
	
def width(): # renvoie la width (largeur) courante du Buffer image
	global Buffer
	return Buffer.width 
	

def height(): # renvoie le height (hauteur) courante du Buffer image
	global Buffer
	return Buffer.height
	

### AUDIO / VOIX ###

PICO   = 'pico'
ESPEAK = 'espeak'

### Audio ###

def playSound(*args):
	
	if len(args) == 0: # si pas de paramètre
		filepathIn = homePath() + "tmpaudio.wav" # fichier par défaut
	else:
		filepathIn = args[0] # sinon, on utilise le chemin reçu 
	
	#print os.path.dirname(filepathIn) # debug
	if os.path.dirname(filepathIn) == '':
		filepathIn = mainPath() + sourcesPath(AUDIO) + filepathIn # chemin par défaut si nom fichier seul
		
	#print filepathIn  #debug
	executeCmdWait("mplayer -msglevel all=-1 " + filepathIn) # seul message erreur cf 0   fatal messages only
	# voir : http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.txt

def playSoundLoop(*args):
	
	if len(args) == 0: # si pas de paramètre
		filepathIn = homePath() + "tmpaudio.wav" # fichier par défaut
	else:
		filepathIn = args[0] # sinon, on utilise le chemin reçu 
	
	#print os.path.dirname(filepathIn) # debug
	if os.path.dirname(filepathIn) == '':
		filepathIn = mainPath() + sourcesPath(AUDIO) + filepathIn # chemin par défaut si nom fichier seul
		
	#print filepathIn  #debug
	executeCmd("mplayer -loop 0 " + filepathIn) # seul message erreur cf 0   fatal messages only

def stopSound():
	# ferme mplayer
	try :
		executeCmdWait("killall mplayer") # ferme mplayer
	except:
		pass
	

def waitSound(*args):
	# ( [seuil], [duree] )
	
	# arg : soit rien, soit duree detect, seuil detect
	if len(args) == 0 :
		executeCmdWait("rec -q trans.wav silence 1 0.1 10% trim 0 1") # seuil 10% pendant 0,1sec - enreg 1 sec..
	if len(args) == 2:
		executeCmdWait("rec -q trans.wav silence 1 " + str(args[1]) + " " + str(args[0]) + "% trim 0 1") # seuil n% pendant nsec - enreg 1 sec..
		# attention seuil = arg[0] et duree =arg[1]


### Voix ### 
def speak(textIn, *arg):
	# arg : soit rien, soit ESPEAK ou PICO
	if len(arg) == 0 : # si pas précisé = pico par defaut 
		executeCmdWait("pico2wave -l fr-FR -w " + homePath() + "pico.wav " + "\"" + str(textIn) + "\"") # encadre chaine de " "
		executeCmdWait("mplayer -msglevel all=-1 " + homePath() + "pico.wav " )
	elif len(arg) == 1 : # sinon, on utilise le moteur tts voulu
		if arg[0] == PICO:
			executeCmdWait("pico2wave -l fr-FR -w " + homePath() + "pico.wav " + "\"" + str(textIn) + "\"") # encadre chaine de " "
			executeCmdWait("mplayer -msglevel all=-1 " + homePath() + "pico.wav " )
		elif arg[0] == ESPEAK:
			#executeCmdWait("espeak -v fr -s 140 "+"\""+str(textIn)+"\" &> /dev/null" ) # &> /dev/null pour pas messages warning
			# appel direct de la commande car >/dev/null ne marche pas sinon
			FNULL = open(os.devnull, 'w')
			#subprocess.call(['echo', 'foo'], stdout=FNULL, stderr=subprocess.STDOUT)
			cmdEspeak = ['espeak', '-v', 'fr', '-s', '140', str(textIn)]
			#print cmdEspeak # debug
			subprocess.check_call(cmdEspeak, stdout=FNULL, stderr=subprocess.STDOUT)
			# voir : http://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
			

def recordSound(*args):
	# args : filepathIn, dureeIn
	
	if len(args) == 0: # si aucun paramètre
		filepathIn = homePath() + "tmpaudio.wav" # fichier par défaut
		dureeIn = 3 # 3 secondes par défaut
	elif len(args) == 1: # si que paramètre de durée
		filepathIn = homePath() + "tmpaudio.wav" # fichier par défaut
		dureeIn = args[0]
	else: # si 2 arguments fichier et durée 
		filepathIn = args[0] # sinon, on utilise le chemin reçu 
		dureeIn = args[1]
	
	if not exists(os.path.dirname(filepathIn)): # cree le rep si existe pas 
		mkdir(os.path.dirname(filepathIn))
	
	executeCmdWait("arecord -d " + str(dureeIn) + " -r 16000 -f cd " + str(filepathIn)) # enregistre 5 secondes en qualite CD a 16000hz dans fichier voulu
	
def analyzeVoice(*args):
	
	# args = filepathIn
	
	if len(args) == 0: # si pas de paramètre
		filepathIn = homePath() + "tmpaudio.wav" # fichier par défaut
	else:
		filepathIn = args[0] # sinon, on utilise le chemin reçu 
		

	workdir = os.path.dirname(filepathIn) + "/" # repertoire du fichier son 
	
	# élimine les silences 
	executeCmdWait("sox " + str(filepathIn) + " " + str(workdir) + "trim.wav silence 1 0.1 1% -1 0.1 1%") # elimine les silences du fichier son
	#print ("sox " + str(filepathIn)+" "+ str(workdir)+"trim.wav silence 1 0.1 1% -1 0.1 1%") # debug
	print "Effacement des silences"
	
	# test duree après effacement silence
	duration = executeCmdOutput("soxi -D " + str(workdir) + "trim.wav") # recupere duree fichier
	#print ("soxi -D "+ str(workdir)+"trim.wav") # debug
	print "duree = " + duration
	
	# si duree insuffisante : sortie de la fonction = evite connexion inutile au serveur
	if float(duration) < 0.1 :
		print "Duree < 0.1 seconde : pas de connexion au serveur !"
		return "" # renvoi chaine vide 
	
	# si la duree est suffisante : la suite est executee = envoi chaine vers serveur vocal 
	
	# formatage du fichier son pour reconnaissance de voix google en ligne 
	executeCmdWait("sox " + str(filepathIn) + " " + str(workdir) + "fichier.flac rate 16k") # convertit le fichier *.wav en fichier *.flac avec echantillonage 16000hz
	#print ("sox " + str(filepathIn)+" "+ str(workdir)+"fichier.flac rate 16k") # debug 
	print "Conversion fichier voix..."
	
	
	out = executeCmdOutput("wget -4 -q -U \"Mozilla/5.0\" --post-file " + str(workdir) + "fichier.flac" + " --header=\"Content-Type: audio/x-flac; rate=16000\" -O  - \"http://www.google.com/speech-api/v1/recognize?lang=fr&client=chromium\" ")
	#print ("wget -4 -q -U \"Mozilla/5.0\" --post-file "+ str(workdir)+"fichier.flac"+" --header=\"Content-Type: audio/x-flac; rate=16000\" -O  - \"http://www.google.com/speech-api/v1/recognize?lang=fr&client=chromium\" ") # debug
	#print out # debug
	print "Connexion serveur reconnaissance vocale..."
	
	# extraction de la chaine reconnue au sein de la reponse google voice a l'aide des expressions regulieres
	result = re.findall(r'^.*\[\{.*:"(.*)",".*$', out) # trouve le texte place --[{--:"**"-- au niveau des **
	print result # debug
	
	if len(result) > 0:
		result = str(result[0])
	else:
		result = ""
	
	print (result) # debug
	return str(result)
	

### VIDEO ###
def playVideo(filepathIn):
	#print os.path.dirname(filepathIn) # debug
	if os.path.dirname(filepathIn) == '':
		filepathIn = mainPath() + sourcesPath(AUDIO) + filepathIn # chemin par défaut si nom fichier seul
		
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
	
### classes utiles multimedia ###

### fin multimedia ###