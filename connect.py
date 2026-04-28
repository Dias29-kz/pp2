import psycopg2
from config import DB_CONFIG

# Create database connection
def get_connection():
    return psycopg2.connect(**DB_CONFIG)
