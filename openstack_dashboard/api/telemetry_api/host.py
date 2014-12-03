class Host:
    def __init__(self, hostname, ip, agent_url, type, services):
        self.__hostname = hostname
        self.__ip = ip
        self.__agent_url = agent_url
        self.__type = type
        self.__services = services

    def get_hostname(self):
        return self.__hostname

    def get_ip(self):
       return self.__ip

    def get_agent_url(self):
        return self.__agent_url

    def get_type(self):
        return self.__type

    def get_services(self):
        return list(self.__services)

def host_from_dict(host_dict):
    hostname = host_dict['hostname']
    ip = host_dict['ip']
    agent_url = host_dict['agent_url']
    node_type = host_dict['type']
    services = []

    for service in host_dict['services']:
        name = service['name']
        type = service['type']
        id = service['id']
        label = service['label']

        services.append(HostService(name, type, id, label))

    return Host(hostname, ip, agent_url, node_type, services)

def hosts_from_dict_list(host_dict_list):
    hosts = []
    for host in host_dict_list:
        hosts.append(host_from_dict(host))

    return hosts

class HostService:
    def __init__(self, name, type, id, label):
        self.__name = name
        self.__type = type
        self.__id = id
        self.__label = label

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_id(self):
        return self.__id

    def get_label(self):
        return self.__label

