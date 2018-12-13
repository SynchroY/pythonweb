import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	"""docstring for Config"""
	SECRET_KEY = 'A Special Key'

	MAIL_SERVER = 'smtp.126.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'xhyzxc10@126.com'
	MAIL_PASSWORD = 'qwertyuiop123'
	MAIL_SUBJECT_PREFIX = '[My_FlaskTest]'
	MYDEFAULT_MAIL_SENDER = 'My_FlaskTest <xhyzxc10@126.com>'
	MYDEFAULT_MAIL_RECIPIENT = 'xhyzxc10@163.com'

	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class Development_Config(Config):
	"""docstring for Development_Config"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = \
	'sqlite:///' + os.path.join(basedir, 'dev_data.sqlite')

class Testing_Config(Config):
	"""docstring for Testing_Config"""
	TEST = True
	SQLALCHEMY_DATABASE_URI = \
	'sqlite:///' + os.path.join(basedir, 'test_data.sqlite')

class Production_Config(Config):
	"""docstring for Production_Config"""
	SQLALCHEMY_DATABASE_URI = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': Development_Config,
	'testing': Testing_Config,
	'production': Production_Config,
	
	'default': Development_Config
}
		