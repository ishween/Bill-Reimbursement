from src.app import app

__author__ = 'ishween'

app.run(debug=app.config['DEBUG'], port=4800)
