import os
from flask import Flask, render_template, session, redirect, url_for, flash 
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap #flask——bootstrap模板扩展
from flask_moment import Moment #flask时间扩展
from flask_wtf import FlaskForm #flask表单扩展
from wtforms import StringField, SubmitField #表单
from wtforms.validators import DataRequired #表单校验器
from flask_sqlalchemy import SQLAlchemy #数据库框架
basedir = os.path.abspath(os.path.dirname(__file__))

from threading import Thread

from flask_migrate import Migrate, MigrateCommand

from datetime import datetime 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'The Key'
app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_mail import Mail, Message
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'xhyzxc10@126.com'
app.config['MAIL_PASSWORD'] = 'qwertyuiop123'
app.config['MAIL_SUBJECT_PREFIX'] = '[My_FlaskTest]'
app.config['MYDEFAULT_MAIL_SENDER'] = 'My_FlaskTest <xhyzxc10@126.com>'
app.config['MYDEFAULT_MAIL_RECIPIENT'] = 'xhyzxc10@163.com'
mail = Mail(app)

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **args):
	msg = Message(subject = app.config['MAIL_SUBJECT_PREFIX']+subject, sender = app.config['MYDEFAULT_MAIL_SENDER'], recipients = [to])
	msg.body = render_template(template + '.txt', **args)
	msg.html = render_template(template + '.html', **args)
	msg_thr = Thread(target = send_async_email, args = [app, msg])
	msg_thr.start()
	return msg_thr

def make_shell_context():
	return dict(app = app, db = db, Role = Role, User = User)
manager = Manager(app)
manager.add_command('shell', Shell(make_context = make_shell_context))


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
	"""docstring for NameForm"""
	name = StringField('What is your name ?', validators = [DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	"""docstring for Role"""
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	users = db.relationship('User', backref = 'role', lazy = 'dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	"""docstring for User"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


@app.route('/', methods = ['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			flash('Looks like you are a new Visitor!')
			if app.config['MYDEFAULT_MAIL_RECIPIENT']:
				send_email(app.config['MYDEFAULT_MAIL_RECIPIENT'], 'New User', 'mail/newuser', user = user)
		else:
			session['known'] = True	
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False), current_time = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name = name, current_time = datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', current_time = datetime.utcnow()),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html', current_time = datetime.utcnow()),500

if __name__ == '__main__':
	#app.run(debug = True)
	manager.run()
