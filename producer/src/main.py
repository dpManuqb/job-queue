import os
import logging
import uvicorn
from fastapi import FastAPI, Request, Response
from src.job import JobProducer

LOG_LEVEL = os.getenv("LOGLEVEL", "DEBUG")

logging.basicConfig(level="ERROR")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

app = FastAPI()

@app.api_route("/healthz", methods=["GET"])
def health():
    """Health endpoint"""
    logger.debug("Health Ok")
    return Response(content="OK", status_code=200)

@app.api_route("/job", methods=["POST"])
async def post_job(request: Request):
    """Endpoint to submit one job"""
    data = await request.json()

    try:
        producer = JobProducer()
        _id = producer.add_job(data)
        producer.close()
        return Response(content=_id, status_code=202)

    except Exception as e:
        logger.error(e)
        return Response(f"Some error ocurred", status_code=500)

@app.api_route("/job/batch", methods=["POST"])
async def post_job_batch(request: Request):
    """Endpoint to submit several jobs at once"""
    data = await request.json()

    try:
        producer = JobProducer()
        _ids = producer.add_batch(data)
        producer.close()
        return Response(content=str(_ids), status_code=202)

    except Exception as e:
        logger.error(e)
        return Response(f"Some error ocurred", status_code=500)

@app.api_route("/job/{_id}", methods=["GET"])
def get_status_job(_id: str):
    """Endpoint to get job status"""
    try:
        producer = JobProducer()
        status = producer.job_status(_id)
        producer.close()
        return Response(content=status, status_code=200)

    except Exception as e:
        logger.error(e)
        return Response(f"Some error ocurred", status_code=500)


if(__name__ == "__main__"):
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")