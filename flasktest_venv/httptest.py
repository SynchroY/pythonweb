from flask import Flask,request
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/test')
def test():
	msg = request.args.get('data')
	return msg
	
if __name__ == '__main__':
	manager.run()