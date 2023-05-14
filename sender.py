import time
import os
import random
import struct
from socket import *

host = "192.168.1.13"
port = 12000
timeout = 5

maximum_segment_size = 200

sequence_number = 1
timestamp = int(time.time())
file_id = random.randint(0, 5)
tail = 0
rtt_old = 1
dev_old = 0.5

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(timeout)

filename = 'hi.txt'

def knowing_the_file(maximum_segment_size, filename):
    file = open(filename, "r")
    file_data_size = os.path.getsize(filename)
    return file_data_size


file_data_size = knowing_the_file(maximum_segment_size, filename)

file_data_of_funct = file_data_size / maximum_segment_size 

with open(filename, 'r') as f:
    words = f.read()

# loop over the file data
while file_data_size >= maximum_segment_size and tail != 1:
    # get the next 200 words
    current_words = words[:maximum_segment_size]
    if (sequence_number == file_data_of_funct):
            tail = 1
            
    # constructing the packet
    packet = struct.pack('!HHiH', sequence_number, file_id, timestamp , tail ) + current_words.encode()

    # sende the packet to the server
    client_socket.sendto(packet, (host, port))

    # wait for the acknowledgment of the previous packet
    try:
        start_time = time.time() # get the  time before sending 

        acknowledgment_packet, server_address = client_socket.recvfrom(2048)
        end_time = time.time()
        acknowledgment_sequence_number, acknowledgment_file_id, acknowledgment_timestamp = struct.unpack('!HHI', acknowledgment_packet)
        print("packet no ", sequence_number, "is received")
        sequence_number += 1

         # get time after receiving the acknowledgment
        rtt_new = end_time - start_time # calculate the RTT
        estimatedTimout  = (1-0.125)* rtt_old + 0.125* rtt_new
        dev_new= (estimatedTimout-rtt_new)
        estimated_div = (1-0.25)*dev_old + 0.25 * dev_new
        new_timeout = estimatedTimout + 4*estimated_div
        # set the timeout to the RTT for the next packet
        client_socket.settimeout(new_timeout)

        # move words to be after the sent words
        words = words[maximum_segment_size:]
        file_data_size -= maximum_segment_size

    except OSError:
        print("Request timed out.")

        continue


client_socket.close()
sender.py
Displaying sender.py.
