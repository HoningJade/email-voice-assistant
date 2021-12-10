"""Backend development configuration."""

import pathlib

BACKEND_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN_DIR = BACKEND_ROOT / "backend" / "token"
TOKEN_FILE = TOKEN_DIR / "token.json"
CREDENTIALS_FILE = TOKEN_DIR / "credentials.json"
NLP_SERVER_PORT = 3001
BACKEND_SERVER_PORT = 3000