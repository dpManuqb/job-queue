import os
import logging
from typing import Dict
from pyhocon import ConfigFactory
from redis import Redis
from rq import Queue
from rq.job import Job

LOG_LEVEL = os.getenv("LOGLEVEL", "DEBUG")
CONFIG_PATH = os.getenv("CONFIG_PATH")

logging.basicConfig(level="ERROR")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

class JobProducer:
    def __init__(self):
        if("http" in CONFIG_PATH):
            self.config = ConfigFactory().parse_URL(CONFIG_PATH)
        else:
            self.config = ConfigFactory().parse_file(CONFIG_PATH)
        self.conn = Redis(host=self.config["redis.host"], port=int(self.config["redis.port"]))

    def add_job(self, data: Dict):
        """Enqueue new job in a queue"""
        q = Queue(connection=self.conn, name=f"queue_{data.get('priority', 5)}")
        job = q.enqueue(data["class"], data["args"])
        return job.id

    def add_batch(self, data: Dict):
        """Enqueue jobs defined in data"""
        q = Queue(connection=self.conn, name=f"queue_{data.get('priority', 5)}")
        job_list = []
        for job in data["jobs"]:
            job_list.append(Queue.prepare_data(job["class"], job["args"]))
        _ids = [j.id for j in q.enqueue_many(job_list)]
        return _ids

    def job_status(self, _id :str):
        """Get job status from the default queue"""
        job =  Job.fetch(_id, connection=self.conn)
        return job.get_status()

    def close(self):
        self.conn.close()