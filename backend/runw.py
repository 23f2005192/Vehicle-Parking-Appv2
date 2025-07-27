from celery import Celery
from tasks import celery

def run_worker():
    celery.start(['worker', '--loglevel=info'])
if __name__ == "__main__":

    run_worker()