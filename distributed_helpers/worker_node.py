import socket
import logging

# Constants
HOST: str = "192.168.1.129"  # Change to IP of Masternode
PORT: int = 12345
BUFFER_SIZE: int = 1024

# Worker node recieve task
# Worker node does work and then worker nodes sends results to db
# Worker node sends back a log of what happened to master node

def send_log():
    pass


def worker_node():
    """
    Defines the functionality of a worker node.
    It requests a task, which it then processeses, then sends the result back to the master node.
    """
    print("\n" + "-" * 50)

    # Requesting a task from the master node
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        worker.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print(
            f"Error: Could not connect to the master node. Check the master node is running and reachable. \n {e} "
        )
        return

    print("\nConnected to master node for task...")
    task = worker.recv(BUFFER_SIZE).decode()
    worker.close()

    # If there's no task available, the worker remains idle
    if task == "NO_TASK":
        print("\nNo task available. Worker is idle.")
        return

    # Fake task
    print(f"\nReceived task: \n{task}\nProcessing...")

    scraped_data = f"Mock data from {task}"

    # Sending processed result back to the master node
    collector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        collector.connect((HOST, PORT + 1))
    except ConnectionRefusedError as e:
        print(
            f"Error: Could not send data to the master node. Check the master node is running and reachable. \n {e} "
        )
        return

    print(f"\nSending mock data to master node for:\n{task}")
    collector.send(scraped_data.encode())
    collector.close()

    print("-" * 50 + "\n")


worker_node()


