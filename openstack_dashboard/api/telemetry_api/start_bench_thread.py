import threading
import ast
import host
from benchmark_agent import start_bench_th

def start_bench_(config):
    hosts = host.hosts_from_dict_list(ast.literal_eval(config.get('Openstack', 'Hosts')), 'compute_node')

    for instance in hosts:
        worker = threading.Thread(target=start_bench_th, kwargs={'projeto':'admin', 'host': instance.get_hostname()})
        worker.daemon = False
        worker.start()
    return 'thread started'
