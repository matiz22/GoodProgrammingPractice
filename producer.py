import argparse
import time
from models import init_db, SessionLocal, Job

def add_job():
    session = SessionLocal()
    try:
        # Create a new job
        new_job = Job()
        session.add(new_job)
        session.commit()
        session.refresh(new_job)
        
        # We simulate the timestamp print format from the original code
        # though it's stored as a datetime object in the DB now.
        timestamp = new_job.created_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Producer: Added job {new_job.id}")
    except Exception as e:
        print(f"Error adding job: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Producer')
    parser.add_argument('--count', type=int, default=1, help='Number of jobs to create')
    args = parser.parse_args()

    init_db()
    for _ in range(args.count):
        add_job()