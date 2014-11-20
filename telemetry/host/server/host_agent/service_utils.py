import subprocess, psutil, inspect
import ConfigParser, ast

def get_service_status(service_list):
    service_status = {}

    for service in service_list:
        p = subprocess.Popen(['service', service['name'], 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        service_status[service['id']] = 'running' in out

    return service_status

def get_process_status(process_list):
    process_status = {}

    for process in process_list:
        process_status[process['name']] = False

    for process in psutil.process_iter():
        if hasattr(process, 'name') and inspect.ismethod(process.name):
            name = process.name()
        else:
            name = process.name

        if name in process_status.keys():
            process_status[name] = True

    for process_name in process_status.keys():
        for process in process_list:
            if process_name == process['name']:
                process_status[process['id']] = process_status.pop(process['name'])

    return process_status
