import subprocess
import argparse
import time
import sys
import signal
from models import init_db

def run_consumers(num_consumers):
    # Ensure DB is created
    init_db()

    processes = []
    print(f"Starting {num_consumers} consumer(s)……")
    
    try:
        for i in range(num_consumers):
            # Launch consumer.py as a separate process
            # We use sys.executable to ensure we use the same python interpreter
            p = subprocess.Popen([sys.executable, '-u', 'consumer.py'])
            processes.append(p)
            print(f"Started consumer process {p.pid}")
            
        print("Consumers running. Press Ctrl+C to stop.")
        
        # Keep the main script alive to monitor or wait for interrupt
        while True:
            time.sleep(1)
            # Check if any process died unexpectedly
            for p in processes:
                if p.poll() is not None:
                    print(f"Consumer {p.pid} exited unexpectedly. Restarting……")
                    processes.remove(p)
                    new_p = subprocess.Popen([sys.executable, 'consumer.py'])
                    processes.append(new_p)
                    print(f"Started new consumer process {new_p.pid}")

    except KeyboardInterrupt:
        print("\nStopping consumers……")
        for p in processes:
            p.terminate()
        
        # Wait for them to exit
        for p in processes:
            p.wait()
        print("All consumers stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run multiple consumers')
    parser.add_argument('--consumers', type=int, default=3, help='Number of consumers to run')
    args = parser.parse_args()
    
    run_consumers(args.consumers)