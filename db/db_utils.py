import psycopg2
from config.config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)