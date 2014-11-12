Collector Service
-----------------

Collect data from each host (provided by Host Agent Server) and store on database.

Usage: 
python collector-service [--debug, --help]

--debug: toggles debug mode ON. If enabled, collector service status details will available on stdout. Debug stdout output example:
hostname: compute3
ip: 10.1.0.82
type: compute_node
agent_url: http://10.1.0.82:6556/host_data
data: {u'memory': [{u'percent': 9.6}], u'disk': [{u'device': u'/', u'percent': 5.0}], u'network': [{u'net_bytes_sent': 7689531840, u'net_bytes_recv': 6397249121}], u'cpu': 1.6}
db: None

--help: show this message.