import socket
import select
import sys
from thread import *

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

IP_address = '127.0.0.1'
Port=8081
server.bind((IP_address,Port))
server.listen(100)

list_of_clients=[]

def clientthread(conn,addr):
	while True:
		try:
			message=conn.recv(1024)
			if message:
				print "<" + addr[0] +"> " + message
				#message_to_send= "<" + addr[0] +"> " + message
				with open(message,'w+') as file_to_write:
					print "telah membuat file"
					
					while True:
						data=conn.recv(1024)
						print data
						print ">menunggu data"
						
						print ">menerima data"
						file_to_write.write(data)
						if not data:
							print "tidak ada data"
							break
						print ">menulis data ke file"
						#file_to_write.write(data)
						#data=conn.recv(1024)
						file_to_write.close()
						break
				print ' receive success'
				broadcast(message,data,conn)
			else:
				remove(conn)
		except:
			continue

def broadcast(message,data,connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:

				clients.send(message)
				with open(message,'rb') as file_to_send:
					#for data in file_to_send:
					#	server.sendall(data)
					data=file_to_send.read(1024)
					while(data):
						print data
						clients.send(data)
						data=file_to_send.read(1024)
						file_to_send.close()
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn,addr=server.accept()
	list_of_clients.append(conn)
	print addr[0] + " connected"
	start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()