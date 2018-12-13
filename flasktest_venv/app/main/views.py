from flask import current_app, render_template, session, redirect, url_for, flash 
from datetime import datetime

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route('/', methods = ['GET', 'POST'])
def index():
	app = current_app._get_current_object()
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
		return redirect(url_for('.index'))
	return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False), current_time = datetime.utcnow())
