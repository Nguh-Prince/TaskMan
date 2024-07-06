import socket
import threading
import psutil
import time
import pickle

class Server:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = cls()
        
        return cls.__instance

    def __init__(self) -> None:
        self.observers = set()
        self.running_processes = set()

    def register_observer(self, observer):
        self.observers.add(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            try:
                observer.send(pickle.dumps(message))
            except Exception as e:
                print(f"Error sending to observer {e}")
                self.observers.remove(observer)

    def monitor_processes_and_services(self):
        while True:
            pass

    def start(self, host='localhost', port=5678):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        threading.Thread(target=self.monitor_processes_and_services, daemon=True).start()

        while True:
            client_socket, address = server_socket.accept()
            self.register_observer(client_socket)
