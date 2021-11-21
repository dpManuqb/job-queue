import os

wsgi_app = "src.main:app"
bind = "0.0.0.0:8080"
worker_class = "uvicorn.workers.UvicornWorker"

workers = int(os.getenv("WORKERS", "4"))
threads = int(os.getenv("THREADS", "2"))
loglevel = os.getenv("LOGLEVEL", "DEBUG")
