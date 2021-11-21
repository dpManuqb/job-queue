import os
import logging
from typing import Dict
from pyhocon import ConfigFactory
from redis import Redis
from rq import Queue
from rq.job import Job

LOG_LEVEL = os.getenv("LOGLEVEL", "DEBUG")

logging.basicConfig(level="ERROR")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class JobProducer:
    def __init__(self):
        self.config = ConfigFactory().parse_file("config/app.conf")
        self.conn = Redis(host=self.config["redis.host"], port=int(self.config["redis.port"]))

    def add_job(self, job: str, payload):
        """Enqueue new job in the default queue"""
        q = Queue(connection=self.conn)
        job = q.enqueue(job, payload)
        return job.id

    def job_status(self, _id :str):
        """Get job status from the default queue"""
        job =  Job.fetch(_id, connection=self.conn)
        return job.get_status()

    def close(self):
        self.conn.close()