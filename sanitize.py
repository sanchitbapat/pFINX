import socket
import re
import urlparse
import sys
from cStringIO import StringIO

class MessageError(Exception): pass

class MessageReader(object):
    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''

    def get_until(self,what):
        while what not in self.buffer:
            if not self._fill():
                return b''
        offset = self.buffer.find(what) + len(what)
        data,self.buffer = self.buffer[:offset],self.buffer[offset:]
        return data

    def get_bytes(self,size):
        while len(self.buffer) < size:
            if not self._fill():
                return b''
        data,self.buffer = self.buffer[:size],self.buffer[size:]
        return data

    def _fill(self):
        data = self.sock.recv(1024)
        if not data:
            if self.buffer:
		sys.exit(1)
            return False
        self.buffer += data
        return True

def conn():
#Wait for a connection on a port
	local_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	local_socket.bind(("localhost", 9011))
	dummy_port="8080"

	while True:
		local_socket.listen(5)
		(client_socket,address)=local_socket.accept()
		mr = MessageReader(client_socket)
#Read the data (request header)
		header = mr.get_until(b'\r\n\r\n')
		san="%27\+OR\+1%3D1--";
		body=''
		if 'Content-Length:' in header and 'POST' in header:
			length=int(re.findall(b'Content-Length: (\w+)',header)[0])
			body = mr.get_bytes(length)
#Sanitize the input (' OR 1=1--)
			body=re.sub(san,'',body);
			print "\n\nBody\n\n %s" % body
		host = re.search(b'host: (\S+)',header)
		hostname = client_socket.getsockname()[0]
		port =client_socket.getsockname()[1]
#Replace the port with the actual one;
		header=header.replace(hostname+":"+str(port), hostname+":"+str(dummy_port))
		header=header.replace("9020","8080")
		print "\n\nMessage\n\n %s" % header

#Create a connection to the server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((hostname , 8080))
		messageHeader=header[:header.index("User-Agent")]+"\r\n"
#Send data on the server (With sanitized input)
		try :
		     s.sendall(header+body)
		except socket.error:
		    sys.exit()
		fullReply=""
		while True:
			reply = s.recv(4096)
			if not reply:break
			fullReply=fullReply+reply
			if "It works" in reply:
				print "\n\nAfter %s\n\n" % reply
#Receive reply and perform output sanitization
		replacedReply=fullReply.replace("Hello","You have just been erased!")
#Send back the reply to the user
		client_socket.send(replacedReply)
	s.close();
	local_socket.close()
conn()
