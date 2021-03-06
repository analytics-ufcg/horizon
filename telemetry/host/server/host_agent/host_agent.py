import time, datetime, psutil, service_utils

def host_data(interval=1, percpu=False, services=None):
    memory = []
    network_data = get_network_data()
    cpu = get_cpu_percent(interval, percpu)
    memory.append(get_virtual_memory())
    disk = get_disk_usage()
    services = get_services_status(services)

    return {"cpu":cpu, "memory":memory, "disk":disk, "network":network_data, "services":services}

def get_cpu_percent(interval, percpu):
    return psutil.cpu_percent(interval, percpu)

def get_virtual_memory():
    memory = {}
    memory["percent"] = psutil.virtual_memory().percent

    return memory

def get_network_data():
    network = []
    net_io_counters = psutil.net_io_counters()
    network_data = {}
    network_data['net_bytes_sent'] = net_io_counters[0]
    network_data['net_bytes_recv'] = net_io_counters[1]
    
    network.append(network_data)

    return network

def get_disk_usage():
    disks = []
    devices = len(psutil.disk_partitions())

    for i in range(devices):
        disk_device_data = {}
        path = psutil.disk_partitions()[i].mountpoint
        disk_device_data["device"] = path
        disk_device_data["percent"] = psutil.disk_usage(path).percent
        
        disks.append(disk_device_data)
        
    return disks

def get_services_status(services):
    services_status = {}

    service_list = []
    process_list = []

    for service in services:
        if service['type'] == 'service':
            service_list.append(service)

        if service['type'] == 'process':
            process_list.append(service)


    services_status.update(service_utils.get_service_status(service_list))
    services_status.update(service_utils.get_process_status(process_list))

    return services_status
