"""Backend package initializer."""
import os
print(os.path.dirname(os.path.abspath(__file__)))
import flask
import backend.ezgmail as ezgmail
from backend.config import TOKEN_FILE, CREDENTIALS_FILE

# app is a single object used by all the code modules in this package
app = flask.Flask("backend")  # pylint: disable=invalid-name
app.config.from_object('backend.config')

ezgmail.init(tokenFile=TOKEN_FILE, credentialsFile=CREDENTIALS_FILE)

import backend.api
import backend.views
