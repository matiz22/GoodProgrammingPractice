import csv
import time
import os
import fcntl
import sys

DB_FILE = 'jobs.csv'

def acquire_lock(file_obj):
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)

def release_lock(file_obj):
    fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)

def get_and_start_job():
    """
    Scans the file for a 'pending' job.
    If found, marks it 'in_progress' and returns the job ID.
    Returns None if no pending job found.
    """
    if not os.path.exists(DB_FILE):
        return None

    target_job_id = None
    rows = []
    
    # We need to Open Read+Write to lock, read, then potentially rewrite
    with open(DB_FILE, 'r+', newline='') as f:
        acquire_lock(f)
        try:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                return None
            
            rows.append(header)
            
            # Read all rows
            data_rows = list(reader)
            
            for row in data_rows:
                # row structure: id, status, created_at
                if target_job_id is None and row[1] == 'pending':
                    target_job_id = row[0]
                    row[1] = 'in_progress'
                rows.append(row)
            
            if target_job_id:
                # Rewind and write everything back
                f.seek(0)
                f.truncate()
                writer = csv.writer(f)
                writer.writerows(rows)
                f.flush()
                os.fsync(f.fileno())
                print(f"Consumer {os.getpid()}: Picked up job {target_job_id}")
            
        finally:
            release_lock(f)
            
    return target_job_id

def finish_job(job_id):
    """
    Marks the specific job as 'done'.
    """
    rows = []
    with open(DB_FILE, 'r+', newline='') as f:
        acquire_lock(f)
        try:
            reader = csv.reader(f)
            rows = list(reader)
            
            found = False
            for row in rows:
                if row[0] == job_id:
                    row[1] = 'done'
                    found = True
                    break
            
            if found:
                f.seek(0)
                f.truncate()
                writer = csv.writer(f)
                writer.writerows(rows)
                f.flush()
                os.fsync(f.fileno())
                print(f"Consumer {os.getpid()}: Finished job {job_id}")
                
        finally:
            release_lock(f)

def run():
    print(f"Consumer {os.getpid()} started.")
    while True:
        job_id = get_and_start_job()
        
        if job_id:
            # Simulate work
            print(f"Consumer {os.getpid()}: Processing {job_id} (will take 30s)...")
            time.sleep(30)
            finish_job(job_id)
        else:
            # Wait before checking again
            time.sleep(5)

if __name__ == "__main__":
    run()
