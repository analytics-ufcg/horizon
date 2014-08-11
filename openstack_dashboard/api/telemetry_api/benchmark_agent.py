import json, requests, time
from telemetry_data import DataHandler
from benchmark_data import BenchmarkDataHandler

def start_bench_th(projeto):
    dados = DataHandler()
    bench = BenchmarkDataHandler()
    dados.start_instance_bench('admin')

    while True:
        try:
            if dados.get_benchmark_status('admin') == 'True':
                break
            time.sleep(5)
        except:
            continue

    read_benchmark = json.loads(dados.get_benchmark('admin')[0])
    read_benchmark['Host'] = '150.165.15.4'
    
    bench.save_data_db(read_benchmark)
    dados.remove_benchmark_instance()
    return read_benchmark

