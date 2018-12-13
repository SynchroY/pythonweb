from flask import Flask,request
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/test',methods=['GET','POST'])
def test():
    if request.method  == 'GET':
        msg = request.args.get('data')
    else:
        msg = request.form.get('data')
    return msg

if __name__ == '__main__':
    manager.run()

