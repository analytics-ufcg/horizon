import json, requests, time
from telemetry_data import DataHandler
from benchmark_data import BenchmarkDataHandler
import ConfigParser

def start_bench_th(projeto, host):
    config = ConfigParser.ConfigParser()
    config.read("environment.conf")
    dados = DataHandler(config)
    bench = BenchmarkDataHandler()
    dados.start_instance_bench('admin', host)
    while True:
        try:
            if dados.get_benchmark_status('admin', host) == 'True':
                break
            time.sleep(5)
        except:
            continue

    read_benchmark = json.loads(dados.get_benchmark('admin', host)[0])
    read_benchmark['Host'] = host
    
    bench.save_data_db(read_benchmark)
    dados.remove_benchmark_instance(host)
    return read_benchmark

