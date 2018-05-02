from base import create_app
from config import config

app = create_app(config['development'])

if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=5000)
