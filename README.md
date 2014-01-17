Librairie Pyduino
=======

## Intro

La librairie Pyduino apporte une couche d'abstraction au langage Python afin de pouvoir utiliser les broches E/S de mini-PC tels que RaspberryPi ou le pcDuino avec des instructions identiques au langage Arduino. 

## Versions disponibles

La librairie existe en plusieurs versions : 

* en version standard qui implémente : 
	* les fonctions Arduino standards
	* les fonctions système (console, ligne de commande)
	* les fonctions de gestion des fichiers et données texte (équivalent librairie SD)
	* les fonctions de gestion du réseau (équivalent de la librairie Ethernet) 
	* les fonctions UART
	* à venir : les fonctions SPI, I2C
	* à venir : les motorisations : moteurs CC, servomoteurs, pas à pas

* en version multimédia qui implémente en plus : 
	* la capture d'image, l'inscrustation de texte dans image
	* la lecture de fichier sons (bruitages, etc...) à partir de fichiers aux formats standards 
	* la capture audio
	* la synthèse vocale
	* la reconnaissance vocale en mode connecté
	* à venir : reconnaissance de lettres dans image, détection objet coloré dans image.. 

## Plateformes supportées : 

* La librairie Pyduino est portée sur les bases mini-pc suivantes : 
	* pcDuino (base conseillée)
	* raspberryPi (version en cours de mise en place...)
	* à venir : la cubieboard

* La librairie Pyduino est également portée en version PC standard tournant sous Gnu/Linux Lubuntu. Cette version permet contrôler une carte Arduino connectée au PC !


## Installation 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.Telecharger


## Exemples 

* Les codes d'exemple sont rassemblés ici : https://github.com/sensor56/pyduino-exemples
* Des pages didactiques par plateformes sont disponibles ici : 
 * pcduino : http://www.mon-club-elec.fr/pmwiki_mon_club_elec/pmwiki.php?n=MAIN.PCDUINO

## Documentation officielle 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.HomePage

## Fonctions Arduino implémentées 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.ReferenceEtendue

## Utilisation 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.DebuterPresentationLogiciel

## Exemple : 

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Juin 2013 - Tous droits réservés - GPLv3
# LED clignote

# entete declarative
LED=2  # declare la broche a utiliser

#--- setup ---
def setup():
        pinMode(LED,OUTPUT) # met la broche en sortie
        Serial.println("La broche " +str(LED)+ " est en sortie !")

# -- fin setup --

# -- loop --
def loop():

        digitalWrite(LED,HIGH) # allume la LED
        Serial.println("La LED est allumée !")

        delay(1000) # pause en millisecondes

        digitalWrite(LED,LOW) # eteint la LED
        Serial.println("La LED est éteinte !")

        delay(1000) # pause en millisecondes


# -- fin loop --



