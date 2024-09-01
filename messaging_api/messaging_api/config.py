import os

SYSTEMDB_USERNAME = os.environ.get("SYSTEMDB_USERNAME","root")
SYSTEMDB_PASSWORD = os.environ.get("SYSTEMDB_PASSWORD","message-system")
SYSTEMDB_ADDR = os.environ.get("SYSTEMDB_ADDR","127.0.0.1")
SYSTEMDB_PORT = int(os.environ.get("SYSTEMDB_PORT","3001"))
SYSTEMDB_DBNAME = os.environ.get("SYSTEMDB_DBNAME","message-system")

BUCKET_ENDPOINT_URL = os.environ.get("BUCKET_ENDPOINT_URL","http://127.0.0.1:3003")
BUCKET_NAME = os.environ.get("BUCKET_NAME","message-system")

API_KEY = os.environ.get("API_KEY", "API_KEY")
REDIS_ADDR = os.environ.get("REDIS_ADDR","127.0.0.1")

