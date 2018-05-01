from unittest import TestCase
from views.base import create_app
from views.config import config

class BaseTestCase():
    def setUp():
    	app = create_app(config['default'])
    	return app.config

print(BaseTestCase().setUp())
