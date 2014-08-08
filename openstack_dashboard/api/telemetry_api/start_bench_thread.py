import threading, ast, ConfigParser
from benchmark_agent import start_bench_th

def start_bench_(config):
    hosts = ast.literal_eval(config.get('Openstack', 'computenodesmap'))
    host_names =  hosts.keys()
    for instance in host_names:
        worker =  threading.Thread(target=start_bench_th, kwargs={'projeto':'admin', 'host': instance})
        worker.daemon = False
        worker.start()
    return 'thread started'
