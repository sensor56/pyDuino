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
	* les fonctions gestion de servomoteurs (équivalent librairie Servo)
	* les fonctions de gestion d'un afficheur LCD (équivalent librairie LiquiCrystal)
	* à venir : les fonctions SPI, I2C
	* à venir : les motorisations : moteurs CC, pas à pas

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

* La librairie Pyduino est également disponible en version "light" c'est à dire sans les fonctions de gestion des broches E/S : cette version permet donc d'utiliser toutes les fonctions Pyduino pour réaliser du développement "classique" sur un PC. 

* Bon à savoir : la librairie Pyduino est également utilisable en tant que module Python classique au sein d'un code Python et permet notamment un appel direct des fonctions Pyduino au sein d'un code PyQt par exemple. Ainsi, lors d'un appui sur un bouton graphique par exemple, on pourra appeler la fonction digitalWrite(broche, HIGH), etc... Quelques exemples d'interfaces PyQt intégrant les fonctions Pyduino ici : http://www.mon-club-elec.fr/pmwiki_mon_club_elec/pmwiki.php?n=MAIN.PCDUINO#toc8

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

## Exemples : 

http://www.mon-club-elec.fr/pmwiki_reference_pyduino/pmwiki.php?n=Main.ApprendreExemples
http://www.mon-club-elec.fr/pmwiki_mon_club_elec/pmwiki.php?n=MAIN.PCDUINO#toc7





