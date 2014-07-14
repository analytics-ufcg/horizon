import threading
from benchmark_agent import start_bench_th

def start_bench_():
    worker =  threading.Thread(target=start_bench_th, kwargs={'projeto':'admin'})
    worker.daemon = False
    worker.start()
    return 'thread started'

