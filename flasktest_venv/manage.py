from app import create_app, db
from app.models import Role, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

import socket, threading

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(5)
'''

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app = app, db = db, Role = Role, User = User)
manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

'''
def tcplink():
	sock, addr = s.accept()
	while True:
		sock.send('welcome!')
		msg = sock.recv(1024)
		sock.send(('hello,%s'%msg.decode('utf-8')).encode('utf-8')) 
'''

'''
class MyTCPHandler(socketserver.BaseRequestHandler):
	"""docstring for MyTCPHandler"""
	def handle(self):
		while True:
			try:
				self.data = self.request.recv(1024).strip()
				self.request.sendall(self.data.upper())
			except ConnectionResetError as e:
				print('err',e)
				break
'''

if __name__ == '__main__':
	#HOST, PORT = '0.0.0.0', 50000
	#server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	manager.run()
#	t = threading.Thread(target = tcplink, args = ())
#	t.start()
	