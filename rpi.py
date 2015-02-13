############## Pyduino RPI ##############

# www.mon-club-elec.fr - Licence GPLv3

print("Pyduino for Raspberry Pi - by www.mon-club-elec.fr - 2015 ")

#-- pour PWM - accès kernel + transposition C to Python --
import fcntl # module pour fonction ioctl
#from ctypes import *
import ctypes # module pour types C en Python

from hardware_rpi import *

"""
LOW =  0

DEC=10
BIN=2
HEX=16
OCT=8

# pour uart
UART="3"
RX=0
TX=1

uartPort=None


# constantes Pyduino
noLoop=False 
debug=False # pour message debug

READ="r"
WRITE="w"
APPEND="a"
"""
"""
#--- chemin de reference ---
#user_name=getpass.getuser()
home_dir=os.getenv("HOME")+"/" # chemin de référence
main_dir=os.getenv("HOME")+"/" # chemin de référence

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
"""
