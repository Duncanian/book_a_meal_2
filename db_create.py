from base import create_app
from config import config
from models.models import db

app = create_app(config['default'])
app_context = app.app_context()
app_context.push()
db.create_all()
