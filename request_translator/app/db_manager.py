from app.logger import setup_logger
from pymongo import MongoClient, errors
import time


class DatabaseManager:
    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri
        self.logger = setup_logger("database_manager")
        self.client = self.connect_to_mongodb()
        self.db = self.client.monarch

    def connect_to_mongodb(self, max_retries=5, wait_time=5):
        attempt = 0
        while attempt < max_retries:
            try:
                self.logger.info(f"Attempt {attempt + 1} to connect to MongoDB at {self.mongodb_uri}")
                client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
                # Attempt to fetch the server info to ensure connection is established
                client.server_info()
                self.logger.info("Successfully connected to MongoDB")
                return client
            except errors.ServerSelectionTimeoutError as e:
                self.logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(wait_time)
        self.logger.error(f"Could not connect to MongoDB after {max_retries} attempts")
        exit(1)
