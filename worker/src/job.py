import time
from typing import Dict
import requests
import math

def wait(time_s: int):
    time.sleep(time_s)
    return f"Waited {time_s} seconds!"

def health():
    return "Ok"

def check_prime(args: Dict):
    max_try = int(math.ceil(math.sqrt(args["number"])))
    data_size = int(max_try / args["parallelism"])

    _range_prime_check_jobs = {"jobs":[]}
    for i in range(args["parallelism"]):
        _range_prime_check_jobs["jobs"].append(
            {
                "class": "job.range_prime_check",
                "args": [{
                    "start": i*data_size,
                    "stop": (i+1)*data_size
                }]
            }
        )
    result = requests.post("http://producer:8080/job/batch", json=_range_prime_check_jobs, headers={"Connection": "Keepalive"})

    _merge_primes_job = {
        "class": "job.merge_prime",
        "args": {
            "_ids": result.content
        }
    }
    requests.post("http://producer:8080/job", json=_merge_primes_job, headers={"Connection": "Keepalive"})

def range_prime_check(args: Dict):
    result = {}
    for i in range(args["start"], args["stop"]):
        result[i] = args["number"] % i == 0

    return result