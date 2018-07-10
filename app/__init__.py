from __future__ import print_function
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('settings')
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

db = SQLAlchemy(app)

from app.V1 import v1

app.register_blueprint(v1)

if __name__ == "__main__":
    app.run(debug=True)
