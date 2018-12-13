import serial
import binascii
import _thread
import struct
import numpy as np

ser = serial.Serial()
i = 0
j = 0
AmpMax = 20
Amp1 = 10
f1 = 60
fs = 20000
imax = 2048
datalist=[]
 
def port_open():
    ser.port = "com4"            #设置端口号
    ser.baudrate = 115200     #设置波特率
    ser.bytesize = 8        #设置数据位
    ser.stopbits = 1        #设置停止位
    ser.parity = "N"        #设置校验位
    ser.timeout = 0.5
    ser.open()              #打开串口,要找到对的串口号才会成功
    if(ser.isOpen()):
        print("打开成功")
    else:
        print("打开失败")
 
def port_close():
    ser.close()
    if (ser.isOpen()):
        print("关闭失败")
    else:
        print("关闭成功")
 
def send(send_data):
    if (ser.isOpen()):
        ser.write(send_data.encode('utf-8'))  #utf-8 编码发送
        #ser.write(binascii.a2b_hex(send_data))  #Hex发送
        print("发送成功",send_data)
    else:
        print("发送失败")
 

def read():
	msg=''
	while True:
		data = (ser.readline()).decode('utf-8')
		msg+=data
		print(msg)
		
		
if __name__ == "__main__":
	port_open()
	_thread.start_new_thread(read,())
	i = 0
	while (i<imax):
		i = i + 1
		value = Amp1/AmpMax*np.sin(2*np.pi*f1*i/fs)*np.power(2,14)+np.power(2,14)
		value = value.astype(int)
		data = struct.pack('>l',value)
		ser.write(data)
	print('发送成功')
	while True:
		j = j+1
	#port_close()