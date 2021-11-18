from redis import Redis
from rq import Queue
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6397")

if(__name__ == "__main__"):
    q = Queue(connection=Redis(host=REDIS_HOST, port=int(REDIS_PORT)))
    q.enqueue("job.sample_dummy_job", 10)