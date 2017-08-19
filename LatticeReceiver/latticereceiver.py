#!/usr/bin/python

#
# Sample UDP OPC receiver program
# Receives multicasted frames from Mystopia/fadecandy server
# https://stackoverflow.com/questions/603852/multicast-in-python
#

import sys
import socket
import struct
import array
import math
import time 
import opc

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DEBUG = True;

INPUT_FRAME_W = 64;   # Dimensions of the incoming matrix (i.e. LED wall)
INPUT_FRAME_H = 32;   #
OUTPUT_FRAME_W = 58;  # Dimensions of the outpu matrix (i.e. chandelier or hat)
OUTPUT_FRAME_H = 5;   #

MCAST_GRP = '224.0.51.51'
MCAST_PORT = 12345
LOCAL_FADECANDY_PORT = 6789

# Frame pixel matrix * rgb 
# + 4 bytes for header 
# information.
MESSAGE_HEADER = 4;
MESSAGE_SIZE = INPUT_FRAME_W * INPUT_FRAME_H *3 + MESSAGE_HEADER; 

DEMO_MODE = False

# Setup to receive UDP Multicast packets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
									# to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Setup connection to local FadeCandy
fc = opc.Client('localhost:{}'.format(LOCAL_FADECANDY_PORT))



def bytesToTuples(data):
	array = []
	for x in range(0, len(data)/3):
		array.append(
			# Unpack from bytes to decimal groups of three as a time,
			# returned as a 3-tuple corresponding to (r, g, b):
			struct.unpack('!BBB', data[(x * 3):(x * 3 + 3)])
		)
	return array


def scaleImage(image, width, height):
	return image.resize((width, height), Image.ANTIALIAS)


def bufferToImage(buffer):
	# Takes a bytearray/buffer (e.g. r, g, b, r, g, b, r, g, b)
	# and returns a PIL Image.
	return Image.frombuffer('RGB', (INPUT_FRAME_W, INPUT_FRAME_H), buffer)


def imageToBuffer(image):
	# use image.getdata() or image.tobytes()
	return image.tobytes()


def drawDemoFrame(i):
	array = []
	i = i + 0.3
	offset = 30
	for y in range(OUTPUT_FRAME_H):
		for x in range(OUTPUT_FRAME_W):
			r = 0
			g = 0
			r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
			g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
			b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
			r = max(0, min(255, r + offset))
			g = max(0, min(255, g + offset))
			b = max(0, min(255, b + offset))
			array.append((int(r),int(g),int(b)))
	return array


def main():
	print >> sys.stderr, '\nMystopia OPC-UDP Receiver'
	DEMO_MODE = False
	i = 0

	#lastPacketTime = time.time()
	#print lastPacketTime

	while True:
		if DEMO_MODE:
			frame = drawDemoFrame(i)
			fc.put_pixels(frame)
			sock.settimeout(0.3)
			try:
				buffer = sock.recv(MESSAGE_SIZE)[3:]    # Discard the 4-byte header
				DEMO_MODE = False
				print 'Demo mode off - starting network mode.'
			except socket.timeout:
				pass

		else:
			print 'Waiting for network LED data.'
			sock.settimeout(5)
			try:
				buffer = sock.recv(MESSAGE_SIZE)[3:]    # Discard the 4-byte header
			except socket.timeout:
				print 'Timed out - starting demo mode.'
				DEMO_MODE = True



'''
	while True:
		print drawDemoFrame(0.0)
		buffer = sock.recv(MESSAGE_SIZE)[3:]    # Discard the 4-byte header
		image = bufferToImage(buffer)
		resized = scaleImage(image, OUTPUT_FRAME_W, OUTPUT_FRAME_H)
		
		output = bytesToTuples(resized.tobytes())
		#print("Output " + str(len(output)) + " pixels. ")
		fc.put_pixels(output);
		
		#draw = ImageDraw.Draw(resized)
		#resized.show()
'''

if __name__ == "__main__":
	main()




'''
Loop:
		if > time since packet
			draw a demo frame
			send demo frame
		check for recv udp
		if received
			restart timer
			draw packet

'''