import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

QUEUES = [f"queue_{i}" for i in range(int(os.getenv("NUM_QUEUES", "10")))]