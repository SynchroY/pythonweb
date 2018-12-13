from flask_wtf import FlaskForm #flask表单扩展
from wtforms import StringField, SubmitField #表单
from wtforms.validators import DataRequired #表单校验器

class NameForm(FlaskForm):
	"""docstring for NameForm"""
	name = StringField('What is your name ?', validators = [DataRequired()])
	submit = SubmitField('Submit')