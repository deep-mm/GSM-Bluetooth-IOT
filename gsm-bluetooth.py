# Importing the Bluetooth Socket library
import bluetooth
# Importing the GPIO library to use the GPIO pins of Raspberry pi
import RPi.GPIO as GPIO
import serial 
import os, time

# Find a suitable character in a text or string and get its position
def find(str, ch):
for i, ltr in enumerate(str):
if ltr == ch:
yield i

GPIO.setmode(GPIO.BOARD)
# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

host = ""
blue_port = 1 # Raspberry Pi uses port 1 for Bluetooth Communication
# Creaitng Socket Bluetooth RFCOMM communication
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
try:
server.bind((host, blue_port))
print("Bluetooth Binding Completed")
except:
print("Bluetooth Binding Failed")

server.listen(1) # One connection at a time
# Server accepts the clients request and assigns a mac address. 
client, address = server.accept()
print("Connected To", address)
print("Client:", client)
send_data = "Enter 1.Send Message\n2.Receive Message\n3.Stop"
try:
while True:
# Receivng the data. 
data = client.recv(1024) # 1024 is the buffer size.
print(data)
send_data = "Enter 1.Send Message\n2.Receive Message\n3.Stop"

if data == "1":
send_data = "Sending Message...\n"
port.write('AT'+'\r\n')
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('ATE0'+'\r\n') # Disable the Echo
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('AT+CMGF=1'+'\r\n') # Select Message format as Text mode 
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('AT+CNMI=2,1,0,0,0'+'\r\n') # New SMS Message Indications
rcv = port.read(10)
print rcv
time.sleep(1)

# Sending a message to a particular Number

port.write('AT+CMGS="+919004096152"'+'\r\n')
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('Hello User, Message from RPi'+'\r\n') # Message
rcv = port.read(10)
print rcv

port.write("\x1A") # Enable to send SMS
for i in range(10):
rcv = port.read(10)
print rcv

send_data = "Message Sent\n"

elif data == "2":
send_data = "Receiving Message...\n"
port.write('AT'+'\r\n')
port.write("\x0D\x0A")
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('ATE0'+'\r\n') # Disable the Echo
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('AT+CMGF=1'+'\r\n') # Select Message format as Text mode 
rcv = port.read(10)
print rcv
time.sleep(1)

port.write('AT+CNMI=2,1,0,0,0'+'\r\n') # New SMS Message Indications
rcv = port.read(10)
print rcv
time.sleep(1)

ck=1
while ck==1:
rcv = port.read(10)
print rcv
fd=rcv
if len(rcv) and len(rcv)>3: # check if any data received 
ck=12
for i in range(5): 
rcv = port.read(10)
print rcv
fd=fd+rcv # Extract the complete data 

# Extract the message number shown in between the characters "," and '\r'

p=list(find(fd, ","))
q=list(find(fd, '\r'))
MsgNo=fd[p[0]+1:q[1]] 

# Read the message corresponds to the message number
rd=port.write('AT+CMGR='+MsgNo+'\r\n')
msg=''
for j in range(10):
rcv = port.read(20)
msg=msg+rcv
print msg
send_data = msg + "\n"
time.sleep(0.1)
send_data = "Message Received\n"

elif data == "3":
send_data = "Connection Closed.. Thank you\n"
GPIO.cleanup()
# Closing the client and server connection
client.close()
server.close()

else:
send_data = "Enter 1.Send Message\n2.Receive Message\n3.Stop"
# Sending the data.
client.send(send_data) 
except Exception as e:
print(e)
# Making all the output pins LOW
GPIO.cleanup()
# Closing the client and server connection
client.close()
server.close()