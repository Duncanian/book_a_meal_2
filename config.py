class BaseConfig(object):
	"""docstring for BaseConfig"""
	DEBUG = False
	SECRET_KEY = '\x8f\x1e\xf0\x83v\x89\xc8T}\xbcs\x0bf\xcf\xa5\x0b\x07*\x9d)z)\xc2\x9e'
	#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/book_meal'

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False

class TestConfig(BaseConfig):
	"""docstring for TestConfig"""
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/tests'

config = {
    'default': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'base': BaseConfig
}
