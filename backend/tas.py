from celery import Celery
from tasks import celery

def run_worker():
    celery.start(['worker', '--loglevel=info'])

def run_beat():
    celery.start(['beat', '--loglevel=info'])

if __name__ == "__main__":

    run_beat()
    
