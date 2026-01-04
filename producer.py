import csv
import os
import fcntl
import time
import uuid
import argparse

DB_FILE = 'jobs.csv'

def acquire_lock(file_obj):
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)

def release_lock(file_obj):
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', newline='') as f:
            acquire_lock(f)
            writer = csv.writer(f)
            writer.writerow(['id', 'status', 'created_at'])
            f.flush()
            release_lock(f)

def add_job():
    # Open in append mode, but we might need to read if we were using auto-increment IDs.
    # Using UUIDs is safer for concurrent appending.
    
    job_id = str(uuid.uuid4())
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    
    with open(DB_FILE, 'a', newline='') as f:
        acquire_lock(f)
        try:
            writer = csv.writer(f)
            writer.writerow([job_id, 'pending', timestamp])
            f.flush()
            os.fsync(f.fileno())
            print(f"Producer: Added job {job_id}")
        finally:
            release_lock(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Producer')
    parser.add_argument('--count', type=int, default=1, help='Number of jobs to create')
    args = parser.parse_args()

    init_db()
    for _ in range(args.count):
        add_job()
