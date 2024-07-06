import os

import psutil
import dbus
from xdg import DesktopEntry

from objects.objects import *

class ProcessManager:
    @classmethod
    def get_process_icon(cls, process_name):
        """Fetches the icon for a process based on its name using .desktop files."""
        icon_path = None
        for directory in os.environ.get('XDG_DATA_DIRS', '/usr/share').split(':'):
            desktop_files_path = os.path.join(directory, 'applications')
            if os.path.exists(desktop_files_path):
                for root, dirs, files in os.walk(desktop_files_path):
                    for file in files:
                        if file.endswith('.desktop'):
                            try:
                                entry = DesktopEntry.DesktopEntry(os.path.join(root, file))
                                if entry.getName().lower() == process_name.lower():
                                    icon_path = entry.getIcon()
                                    if icon_path and not os.path.isabs(icon_path):
                                        icon_path = os.path.join('/usr/share/icons', icon_path)
                                    return icon_path
                            except Exception:
                                continue
        
        import base64

        if icon_path and os.path.exists(icon_path):
            with open(icon_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read())

                return encoded_string
        else:
            print(f"The path: {icon_path} did not exist")

        return None
    
    @classmethod
    def get_running_processes(cls):
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
                    icon = cls.get_process_icon(name)

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
    
    @classmethod
    def list(cls):
        return cls.get_running_processes()
    
    @classmethod
    def stop(cls, pid):
        """Stops a process with the given PID."""
        try:
            process = psutil.Process(pid)
            process.terminate()  # Send SIGTERM
            process.wait(timeout=3)
            print(f"Process {pid} terminated.")
        except psutil.NoSuchProcess:
            print(f"Process {pid} does not exist.")
        except psutil.TimeoutExpired:
            process.kill()  # Send SIGKILL if process doesn't terminate
            print(f"Process {pid} killed.")
        except Exception as e:
            print(f"Error stopping process {pid}: {e}")

    @classmethod
    def set_priority(cls, pid, priority):
        """Modifies the priority of a process with the given PID."""
        try:
            process = psutil.Process(pid)
            process.nice(priority)
            print(f"Process {pid} priority changed to {priority}.")
        except psutil.NoSuchProcess:
            print(f"Process {pid} does not exist.")
        except psutil.AccessDenied:
            print(f"Access denied when changing priority of process {pid}.")
        except Exception as e:
            print(f"Error changing priority of process {pid}: {e}")

class ServiceManager:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = cls()
        
        return cls.__instance
    
    def __init__(self) -> None:
        """Gets the systemd manager object."""
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        
        self.manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
    
    def start(self, service_name):
        """Starts a systemd service."""
        try:
            self.manager.StartUnit(service_name, 'fail')
            print(f"Service {service_name} started.")
        except Exception as e:
            print(f"Error starting service {service_name}: {e}")

    def stop(self, service_name):
        """Stops a systemd service."""
        try:
            self.manager.StopUnit(service_name, 'fail')
            print(f"Service {service_name} stopped.")
        except Exception as e:
            print(f"Error stopping service {service_name}: {e}")

    def restart(self, service_name):
        """Restarts a systemd service."""
        try:
            self.manager.RestartUnit(service_name, 'fail')
            print(f"Service {service_name} restarted.")
        except Exception as e:
            print(f"Error restarting service {service_name}: {e}")

    def reload(self, service_name):
        """Reloads a systemd service."""
        try:
            self.manager.ReloadUnit(service_name, 'fail')
            print(f"Service {service_name} reloaded.")
        except Exception as e:
            print(f"Error reloading service {service_name}: {e}")