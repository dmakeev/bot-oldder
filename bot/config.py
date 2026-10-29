"""Configuration for the PROсрочка bot."""
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "bot/data/prosrochka.db")
