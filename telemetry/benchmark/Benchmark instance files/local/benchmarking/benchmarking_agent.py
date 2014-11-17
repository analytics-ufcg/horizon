import subprocess

def read_benchmarking():
    arquivo = open('/home/analytics/benchmarking/benchmarking_data.txt','r')
    bench = arquivo.readlines()
    arquivo.close()
    return bench

def start_benchmarking():
    processo = subprocess.Popen('python /home/analytics/benchmarking/benchmarking.py', shell = True, stdout=subprocess.PIPE)
    return 'benchmarking inicializado com sucesso'
