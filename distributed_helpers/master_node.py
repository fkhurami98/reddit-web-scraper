import socket
import threading
from queue import Queue
from pprint import pprint

# Constants
HOST: str = '0.0.0.0'
PORT: int = 12345
BUFFER_SIZE: int = 1024

URLS: list = [
'https://www.reddit.com/r/LifeProTips/comments/15f2fdl/lpt_a_competition_and_final_goodbye_to_awards_on/'
'https://www.reddit.com/r/LifeProTips/comments/15il78f/lpt_always_peel_boiled_eggs_underwater/',
'https://www.reddit.com/r/LifeProTips/comments/15iqc04/lpt_request_today_i_wore_a_new_pair_of_shoes_and/',
'https://www.reddit.com/r/LifeProTips/comments/15hn5i0/lpt_visiting_loved_ones_in_the_hospital_bring/',
'https://www.reddit.com/r/LifeProTips/comments/15irymh/lpt_how_to_stop_having_a_resting_anxious_face/',
'https://www.reddit.com/r/LifeProTips/comments/15isah2/lpt_preventing_egg_from_cracking_during_boiling/',
'https://www.reddit.com/r/LifeProTips/comments/15iti8q/lpt_urgent_request/'
]

# Instintaniate a task_queue using the Queue() class
task_queue = Queue()

# Populating the task queue
for url in URLS:
    task_queue.put(url)

# Instintaniate a empty result list
results = []


def task_distributor():
    """
    This function listens for worker connections and distributes tasks to them.
    """
    distributor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    distributor.bind((HOST, PORT))
    distributor.listen(5)
    print("\nMaster node started, waiting for worker connections...\n" + "-"*50)

    while True:
        worker, addr = distributor.accept()
        print(f"\nConnected to worker @ {addr}\n\n")
        if not task_queue.empty():
            task = task_queue.get()
            print(f"Sending task:\n\n{task}\n\nto worker @ {addr}")
            worker.send(task.encode())
        else:
            print("\nNo tasks available. Sending 'NO_TASK' message to worker.")
            worker.send("NO_TASK".encode())
        worker.close()


def result_collector():
    """
    This function listens for results from workers and collects them.
    """
    collector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    collector.bind((HOST, PORT + 1))
    collector.listen(5)
    print("\nResult collector started, waiting for results...\n" + "-"*50)

    while True:
        worker, addr = collector.accept()
        data = worker.recv(BUFFER_SIZE).decode()
        if data != "NO_TASK":
            results.append(data)
            print(f"\nReceived data from worker @ {addr}:\n\n{data}\n"+ "-"*50 )
        worker.close()


# Starting the distributor and collector threads
threading.Thread(target=task_distributor).start()
threading.Thread(target=result_collector).start()

# Keeping the script running for testing purposes
try:
    while True:
        pass
except KeyboardInterrupt: # Ctrl + C to see results.
    print("\nResults collected:")
    pprint(results)