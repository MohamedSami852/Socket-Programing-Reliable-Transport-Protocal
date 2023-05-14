import time
from socket import *
import struct
import random

host = "192.168.1.13"
port = 12000

serversocket = socket(AF_INET, SOCK_DGRAM)
serversocket.bind((host, port))

seen_sequence_numbers = []

while True:
    packet, address = serversocket.recvfrom(2048)

    # randomly drop 10% of the packets
    if random.randint(1, 100) < 15:
        print("Packet loss, sequence number = ", struct.unpack('!H', packet[:2])[0])
        continue

    sequencenumber, file_id, timestamp, tail = struct.unpack('!HHIh', packet[:10])

    # check if we've seen this sequence number before
    if sequencenumber in seen_sequence_numbers:
        print("Duplicate packet, sequence number = ", sequencenumber)
        continue

    # add this sequence number to the list of seen sequence numbers
    seen_sequence_numbers.append(sequencenumber)

    current_words = packet[10:].decode()
    print(f'Sequence number: {sequencenumber}')
    print(f'File ID: {file_id}')
    print(f'Timestamp: {timestamp}')
    print(f'Data: {current_words}')
    print(f'Tail: {tail}')

    with open('user.txt', 'a') as file:
        for word in current_words:
            file.write(current_words)
            break

    # make the ack. packet
    acknowledgment_packet = struct.pack('!HHI', sequencenumber, file_id, timestamp)

    # Send the ack. packet
    serversocket.sendto(acknowledgment_packet, address)
    if tail == 1:
        print("All of the file has been received successfully")
        break

serversocket.close()
