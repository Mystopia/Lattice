#!/usr/bin/env python
import socket
import sys
import opc 

# Setup connection to FadeCandy
fc = opc.Client('localhost:{}'.format(7890))


# Listen to PixelController via UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 6789
SIZE = 64 * 32 * 3 # w * h * channels; expecting 6144 bytes per message


# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.bind(('localhost', UDP_PORT))


# Parse message data as array of 3-val tuples
def getFrame(data):
  array = []
  for x in range(0, len(data)/3):
    r = data[x * 3]
    g = data[x * 3 + 1]
    b = data[x * 3 + 2]
    array.append((r, g, b))
  return array


# Process udp messages as frames
print >> sys.stderr, '\nWaiting to receive message'
while True:
  data, address = sock.recvfrom(SIZE)
  print >>sys.stderr, 'Received %s values from %s' % (len(data), address)

  frame = getFrame(map(ord, data))
  print >>sys.stderr, 'Outputting a frame with %s tuples' % (len(frame))
  fc.put_pixels(frame)
  