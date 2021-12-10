"""NLP package initializer."""
import os
print(os.path.dirname(os.path.abspath(__file__)))
import flask
from nlp.config import NLP_SERVER_PORT, BACKEND_SERVER_PORT

# app is a single object used by all the code modules in this package
app = flask.Flask("nlp")  # pylint: disable=invalid-name
app.config.from_object('nlp.config')
app.config["SECRET_KEY"] = "voicemail"

import nlp.api
df_sessions = {} # a global dict containing all df sessions, can access each df session by session_id