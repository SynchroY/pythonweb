from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **args):
	app = current_app._get_current_object()
	msg = Message(subject = app.config['MAIL_SUBJECT_PREFIX']+subject, sender = app.config['MYDEFAULT_MAIL_SENDER'], recipients = [to])
	msg.body = render_template(template + '.txt', **args)
	msg.html = render_template(template + '.html', **args)
	msg_thr = Thread(target = send_async_email, args = [app, msg])
	msg_thr.start()
	return msg_thr
