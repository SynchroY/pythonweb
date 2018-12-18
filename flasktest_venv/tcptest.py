import socket, threading
import struct
import numpy as np
import matplotlib.pyplot as plt

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 5000))
s.listen(5)

fs = 20000
N = 2048
AmpMax = 20


def tcplink():
	sock, addr = s.accept()
	wave = ()
	i = 0
	print("连接成功")
	while i<N:
		i = i+1
		print(i)
		msg = sock.recv(4)
		print(msg)
		if (len(msg) == 4):
			value = struct.unpack('>l',msg)
			last_msg = msg
		else:
			value = struct.unpack('>l',last_msg)			
		print(value)
		wave = wave+value
	f = abs(np.fft.fft(wave))
	t = np.arange(N)
	freq = np.fft.fftfreq(t.shape[-1])
	#plt.plot(freq,f)
	#plt.show()
	f[np.argmax(f)] = 0
	if (np.argmax(f)>(N/2)):
		freq0 = (N-np.argmax(f))*fs/N
	else:
		freq0 = np.argmax(f)*fs/N
	mag0 = f[np.argmax(f)]*2/N/np.power(2,14)*AmpMax
	print(mag0)
	print(freq0)
	sock.send(("%s%s%s"%("Base Frequence is ",str(freq0),"Hz\n")).encode())
	sock.send(("%s%s%s"%("Magnitude is ",str(mag0),"\n")).encode())
	sock.close()
	s.close()
	
	
	



		

t = threading.Thread(target = tcplink, args = ())
t.start()
