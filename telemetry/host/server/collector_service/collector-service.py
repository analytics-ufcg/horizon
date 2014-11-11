import sys
import ConfigParser, ast
import requests, time

from host_dbwriter import HostDataDBWriter

config = ConfigParser.ConfigParser()
config.read("environment.conf")

HOSTS = ast.literal_eval(config.get('Openstack', 'computenodes'))

def main(argv):
    store_host_data(hosts=HOSTS, config=config)

def store_host_data(hosts, config):
    server = config.get('Misc', 'dbserver')
    user = config.get('Misc', 'dbuser')
    passwd = config.get('Misc', 'dbpass')
    database = config.get('Misc', 'hostsdbname')
    table = config.get('Misc', 'hostsdbtable')

    db = HostDataDBWriter(server, user, passwd, database, table)

    while True:
        for host in hosts:
            data = get_host_metric(host)

            if(data == 'Unknown host'):
                db.save_data_db(host_status='F', host=host)
                continue

            cpu = data["cpu"]
            memory = data["memory"]
            disk = data["disk"]
            network = data["network"]

            db.save_data_db(cpu=cpu, memory=memory, disk=disk, network=network, host=host)

        time.sleep(60)


def get_host_metric(host):
    url = "http://%s:6556/host_data" % host
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            return 'Unknown host'
    except:
        return 'Unknown host'

if __name__ == "__main__":
   main(sys.argv[1:])