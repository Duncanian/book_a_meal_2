from os import getenv

class BaseConfig(object):
	"""docstring for BaseConfig"""
	DEBUG = False
	#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = getenv('DEVELOPMENT_DATABASE_URI')
	
'''class ProductionConfig(BaseConfig):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/production'
'''

class TestConfig(BaseConfig):
	"""docstring for TestConfig"""
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = getenv('TESTING_DATABASE_URI')

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig
}
