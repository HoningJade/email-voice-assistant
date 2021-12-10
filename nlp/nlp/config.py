"""NLP development configuration."""

import pathlib

BACKEND_ROOT = pathlib.Path(__file__).resolve().parent.parent
NLP_SERVER_PORT = 3001
BACKEND_SERVER_PORT = 3000
PRIVATE_KEY = pathlib.Path(__file__).resolve().parent / "dialogflow" / "private_key" / "test-conv-ai-1011-3b1d693b53da.json"
