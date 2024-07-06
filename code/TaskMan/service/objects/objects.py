from dataclasses import dataclass

@dataclass
class User:
    username: str

@dataclass
class Process:
    pid: int
    ppid: int
    priority: int
    state: str
    nice: int
    tty_nr: int
    session: int
    icon: str
    user: User

@dataclass
class Service:
    name: str

@dataclass
class Resource:
    name: str
    unit: str

class ResourceConsumed:
    resource: str
    quantity: int
    pid: Process