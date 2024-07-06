import psutil
from dataclasses import dataclass
from xdg import DesktopEntry
import os

from objects.objects import *

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'ppid', 'name', 'status', 'nice', 'terminal', 'username']):
        try:
            with proc.oneshot():
                pid = proc.info['pid']
                name = proc.info['name']
                priority = proc.nice()
                state = proc.status()
                nice = proc.info['nice']
                tty_nr = proc.info['terminal']
                session = proc.session_id()
                icon = get_process_icon(name)

                user = User(username=proc.info['username'])

                processes.append(
                    Process(
                        pid=pid, priority=priority, state=state, nice=nice, 
                        tty_nr=tty_nr or -1, session=session, icon=icon, user=user
                    )
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes