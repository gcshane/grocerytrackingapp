from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DB_URL: str = os.getenv("SUPABASE_URL")

config = Config()