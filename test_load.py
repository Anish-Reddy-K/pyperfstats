"""
Simple 15-second test script that increases CPU, memory, and thread usage.
Perfect for quickly testing pyperfstats features.
"""
import time
import math
import random
import threading
import os

# Total duration of the test in seconds
DURATION = 15

def cpu_work(seconds=1):
    """Do some CPU-intensive calculations."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        # Meaningless but CPU-intensive calculations
        for _ in range(10000):
            x = math.sin(random.random()) * math.cos(random.random())
            y = math.sqrt(abs(x)) + math.log(abs(x) + 1)

def allocate_memory(mb=10):
    """Allocate and return a chunk of memory."""
    # Each double is 8 bytes, so we need mb*1024*1024/8 doubles for MB
    chunk_size = int((mb * 1024 * 1024) / 8)
    return [random.random() for _ in range(chunk_size)]

def thread_worker(seconds=1):
    """Function executed by worker threads."""
    time.sleep(seconds / 2)
    cpu_work(seconds / 2)

def create_files(count=3, kb=100):
    """Create temporary files with random data."""
    files = []
    for i in range(count):
        filename = f"temp_{i}.dat"
        with open(filename, 'wb') as f:
            f.write(os.urandom(kb * 1024))
        files.append(filename)
    return files

def main():
    print("Starting 15-second performance test...")
    start_time = time.time()
    end_time = start_time + DURATION
    
    # Hold references to allocated memory
    memory_blocks = []
    temp_files = []
    
    # We'll do 5 steps of increasing resource usage
    step_time = DURATION / 5
    
    try:
        # Step 1: Light CPU usage
        print("Step 1: Light CPU usage")
        cpu_work(1)
        time.sleep(step_time - 1)
        
        # Step 2: Add some memory usage
        print("Step 2: Adding memory usage (50MB)")
        memory_blocks.append(allocate_memory(50))
        cpu_work(1)
        time.sleep(step_time - 1)
        
        # Step 3: Add threads
        print("Step 3: Adding threads")
        threads = []
        for i in range(5):
            t = threading.Thread(target=thread_worker, args=(2,))
            t.daemon = True
            threads.append(t)
            t.start()
        cpu_work(1)
        time.sleep(step_time - 1)
        
        # Step 4: More memory + file operations
        print("Step 4: More memory (100MB) + file operations")
        memory_blocks.append(allocate_memory(100))
        temp_files = create_files(5, 200)
        cpu_work(1.5)
        time.sleep(step_time - 1.5)
        
        # Step 5: Heavy CPU + memory + threads
        print("Step 5: Heavy CPU + more memory (200MB) + more threads")
        memory_blocks.append(allocate_memory(200))
        more_threads = []
        for i in range(10):
            t = threading.Thread(target=thread_worker, args=(2,))
            t.daemon = True
            more_threads.append(t)
            t.start()
        cpu_work(3)
        
        # Wait for the full duration
        remaining = end_time - time.time()
        if remaining > 0:
            time.sleep(remaining)
            
    finally:
        # Clean up temp files
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)
    
    print("Test completed!")

if __name__ == "__main__":
    main()