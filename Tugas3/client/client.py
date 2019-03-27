import socket
import select
import sys
import msvcrt

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP_address='127.0.0.1'	
Port = 8081 
server.connect((IP_address,Port))

while True:
	sockets_list=[server]

	read_sockets,write_socket,error_socket=select.select(sockets_list,[],[],1)
	if msvcrt.kbhit(): read_sockets.append(sys.stdin)

	for socks in read_sockets:
		if socks==server:
			#message=socks.recv(2048)
			#print message
			message=socks.recv(1024)
			if message:
				#print "<" + addr[0] +"> " + message
				#message_to_send= "<" + addr[0] +"> " + message
				with open(message,'w+') as file_to_write:
					print "telah membuat file"
					
					while True:
						data=socks.recv(1024)
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
		else:
			#message=sys.stdin.readline()
			message=raw_input()
			operand,filename=message.split(' ', 1)
			server.send(filename)
			if operand == "SEND":
				with open(filename,'rb') as file_to_send:
					#for data in file_to_send:
					#	server.sendall(data)
					data=file_to_send.read(1024)
					while(data):
						server.send(data)
						data=file_to_send.read(1024)
						file_to_send.close()
				
				sys.stdout.write("<you> ")
				sys.stdout.write(filename)
				sys.stdout.write(" send success")
				sys.stdout.flush()
server.close()