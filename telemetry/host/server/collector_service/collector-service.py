import sys
import ConfigParser, ast
import requests, time

from host_dbwriter import HostDataDBWriter

__DEBUG = False

def main():
    print "Collector Service is up and running..."
    config = ConfigParser.ConfigParser()
    #config.read("/etc/telemetry/collector-service.conf")
    config.read("collector-service.conf")

    hosts = ast.literal_eval(config.get('Openstack', 'ComputeNodes'))
    timeout = ast.literal_eval(config.get('Openstack', 'HostTimeout'))
    timebetweenrequests = ast.literal_eval(config.get('Openstack', 'TimeBetweenRequests'))


    store_host_data(hosts=hosts, config=config, timebetweenrequests=timebetweenrequests, timeout=timeout, debug=__DEBUG)


def store_host_data(hosts, config, timeout, timebetweenrequests, debug=False):
    server = config.get('Misc', 'dbserver')
    user = config.get('Misc', 'dbuser')
    passwd = config.get('Misc', 'dbpass')
    database = config.get('Misc', 'hostsdbname')
    table = config.get('Misc', 'hostsdbtable')

    db = HostDataDBWriter(server, user, passwd, database, table)

    while True:
        for host in hosts:
            data = get_host_metric(host['agent_url'], timeout)

            if data == 'Unknown host':
                print
                result = db.save_data_db(host_status='F', host=host['ip'])
            else:
                cpu = data["cpu"]
                memory = data["memory"]
                disk = data["disk"]
                network = data["network"]

                result = db.save_data_db(cpu=cpu, memory=memory, disk=disk, network=network, host=host['ip'])

            if debug:
                output =  "\nhostname: " + str(host['hostname'])
                output += "\nip: " + str(host['ip'])
                output += "\ntype: " + str(host['type'])
                output += "\nagent_url: " + str(host['agent_url'])
                output += "\nresponse: " + str(data)
                output += "\ndb: " + str(result)
                print output

        time.sleep(timebetweenrequests)


def get_host_metric(agent_url, timeout):
    url = agent_url
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        else:
            return 'Unknown host'
    except:
        return 'Unknown host'

def help(args):
    return """Usage: python """ + args[0] + """ [OPTION...]
      -d, --debug                toggles debug mode ON. If enabled, collector
                                   service status details will available on stdout.
      --help                     display this help and exit
      """

if __name__ == "__main__":
    args = sys.argv
    __DEBUG=('--debug' in args) or ('-d' in args) or __DEBUG

    if '--help' in args:
        print help(args)
    else:
        main()
