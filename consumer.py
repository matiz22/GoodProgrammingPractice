import time
import os
import sys
from sqlalchemy import select, update
from models import SessionLocal, Job, init_db

def get_and_start_job():
    """
    Scans the db for a 'pending' job.
    If found, marks it 'in_progress' and returns the job ID.
    Returns None if no pending job found.
    Uses atomic UPDATE ... RETURNING to ensure concurrency safety.
    """
    session = SessionLocal()
    try:
        # Atomic update: Find a pending job, set it to in_progress, and return its ID
        # This prevents race conditions between consumers
        subq = (
            select(Job.id)
            .where(Job.status == "pending")
            .limit(1)
            .scalar_subquery()
        )
        
        stmt = (
            update(Job)
            .where(Job.id == subq)
            .values(status="in_progress")
            .returning(Job.id)
        )
        
        result = session.execute(stmt)
        row = result.fetchone()
        session.commit()
        
        if row:
            job_id = row[0]
            print(f"Consumer {os.getpid()}: Picked up job {job_id}")
            return job_id
        
        return None
        
    except Exception as e:
        # In case of database lock errors or others, rollback and retry later
        # print(f"Consumer {os.getpid()} error: {e}") 
        session.rollback()
        return None
    finally:
        session.close()

def finish_job(job_id):
    """
    Marks the specific job as 'done'.
    """
    session = SessionLocal()
    try:
        stmt = (
            update(Job)
            .where(Job.id == job_id)
            .values(status="done")
        )
        session.execute(stmt)
        session.commit()
        print(f"Consumer {os.getpid()}: Finished job {job_id}")
    except Exception as e:
        print(f"Consumer {os.getpid()} error finishing job: {e}")
        session.rollback()
    finally:
        session.close()

def run():
    # Ensure tables exist (consumer might start before producer or independently)
    # init_db() # Safe to call multiple times, but main/producer usually handles it. 
    # Calling it here just in case doesn't hurt with create_all.
    
    print(f"Consumer {os.getpid()} started.")
    while True:
        job_id = get_and_start_job()
        
        if job_id:
            # Simulate work
            print(f"Consumer {os.getpid()}: Processing {job_id} (will take 5s)...") # Reduced to 5s for easier testing, was 30s
            time.sleep(5) 
            finish_job(job_id)
        else:
            # Wait before checking again
            time.sleep(5)

if __name__ == "__main__":
    run()