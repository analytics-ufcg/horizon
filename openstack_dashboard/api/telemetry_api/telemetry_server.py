from flask import Flask, render_template, request, make_response

from telemetry_data import DataHandler, MigrateException

import json, requests, threading, ConfigParser, ast

from agent_server import store_host_data

from start_bench_thread import start_bench_ 


LOGFILE = 'telemetry_server'

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read("environment.conf")

HOSTS = ast.literal_eval(config.get('Openstack', 'computenodes'))

data_handler = DataHandler(config)

@app.route('/projects')
def projects():
    resp = make_response(data_handler.projects())
    resp.headers['Access-Control-Allow-Origin'] = "*" 

    return resp

@app.route('/projects/instances')
def project_instances():
    resp = make_response(data_handler.projects_with_instances_and_cpu_util())
    resp.headers['Access-Control-Allow-Origin'] = "*" 

    return resp

@app.route('/hosts')
def hosts():
    data = {'name':'hosts','children':[]}
    for h in HOSTS:
        host = {'ip':h}
        data['children'].append(host)
    resp = make_response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/hosts/instances')
def hosts_instances():
    host_name = request.args.get('host_name', None)

    resp = None
    if not host_name:
        resp = make_response(json.dumps({'error' : 'host name cannot be empty'}), 400)
    else:
        resp = make_response(json.dumps(data_handler.instances_from_host(host_name)))

    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp       

@app.route('/hosts_cpu_util')
def hosts_cpu_util():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    
    resp = make_response(json.dumps(data_handler.hosts_cpu(timestamp_begin, timestamp_end)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

@app.route('/hosts_cpu_util_otimization')
def hosts_cpu_util_otimization():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(json.dumps(data_handler.points_reduction_by_server_cpu(timestamp_begin, timestamp_end,HOSTS)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp


@app.route('/hosts_memory')
def hosts_memory():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    
    resp = make_response(json.dumps(data_handler.hosts_memory(timestamp_begin, timestamp_end)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp


@app.route('/hosts_memory_otimization')
def hosts_memory_otimization():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(json.dumps(data_handler.points_reduction_by_server_memory(timestamp_begin, timestamp_end, HOSTS)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp


@app.route('/hosts_disk')
def hosts_disk():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    
    resp = make_response(json.dumps(data_handler.hosts_disk(timestamp_begin, timestamp_end)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

@app.route('/hosts_disk_otimization')
def hosts_disk_otimization():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(json.dumps(data_handler.points_reduction_by_server_disk(timestamp_begin, timestamp_end, HOSTS)))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp


@app.route('/hosts_recommendation')
def hosts_recommendation():
    r_cpu = hosts_cpu_util()
    r_memory = hosts_memory() 
    r_disk = hosts_disk()

    resp = make_response(data_handler.hosts_recommendation(r_cpu.data, r_memory.data , r_disk.data))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route('/cpu_util')  
def cpu_util():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    resource_id = request.args.get('resource_id', None)
    
    resp = make_response(data_handler.cpu_util_from(timestamp_begin, timestamp_end, resource_id))
    resp.headers['Access-Control-Allow-Origin'] = "*" 

    return resp

@app.route('/cpu_util2')
def cpu_util2():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    resource_id = request.args.get('resource_id', None)
    
    resp = make_response(json.dumps(data_handler.points_reduction_vm(timestamp_begin, timestamp_end,resource_id)))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route('/cpu_util_flavors')
def cpu_util_flavors():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(data_handler.cpu_util_flavors(timestamp_begin, timestamp_end))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

@app.route('/alarms_history')
def alarms_history():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(data_handler.alarms_history(timestamp_begin, timestamp_end))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

@app.route('/add_alarm',  methods=['POST'])
def add_alarm():
    name = request.args.get('name')
    resource = request.args.get('resource')
    operator = request.args.get('operator')
    threshold = request.args.get('threshold')
    period = request.args.get('period')
    evalperiod = request.args.get('evalperiod')
    send_mail = request.args.get('send_mail')

    alarm = data_handler.add_alarm(name, resource, threshold, operator, period, evalperiod, send_mail)
    
    if alarm:
        resp = make_response(json.dumps({'alarm_id' : alarm.alarm_id}))
    else:
        resp = make_response(json.dumps({'alarm_id' : 'null'}))

    resp.headers['Access-Control-Allow-Origin'] = "*" 

    return resp
    
@app.route('/alarm', methods=['POST'])
def alarm():
    data_handler.alarm_email(request.data)
    return 'passou'

@app.route('/alarm_description')
def alarm_description():
    resp = make_response(data_handler.alarm_description())
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/alarm_delete', methods=['POST'])
def alarm_delete():
    alarm_id = request.args.get('alarm_id')
    resp = make_response(data_handler.delete_alarm(alarm_id))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/host_metrics')
def metrics():
    project = request.args.get('project')
    resp = make_response(data_handler.host_metrics(project))
    resp.headers['Access-Control-Allow-Origin'] = "*"

    return resp

@app.route('/live_migration', methods=['POST'])
def live_migration():
    project_name = request.args.get('project')
    host = request.args.get('host_name')
    vm = request.args.get('instance_id')
    try:
        migrate = data_handler.migrate_to_host(project_name,host,vm)
        resp = make_response(json.dumps({'migracao' : 'efetuando'}))
        resp.headers['Access-Control-Allow-Origin']="*"
    except MigrateException, exc:    
        resp = make_response(json.dumps({'migracao': exc.message}),exc.error)
        resp.headers['Access-Control-Allow-Origin']="*"
    return resp

@app.route('/host_migration')
def host_migration_selection():
    hosts_name = request.args.get('hosts')
    if hosts_name == '':
        hosts_list = []
    else:
        hosts_list = hosts_name.split(",")
    migrate = data_handler.suggestion(hosts_list)
    resp = make_response(migrate)
    resp.headers['Access-Control-Allow-Origin']="*"
    return resp

@app.route('/benchmark_data')
def benchmark_data():
    resp = make_response(data_handler.get_benchmark_bd())
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/get_benchmark')
def get_benchmark():
    resp = make_response(data_handler.get_benchmark('admin'))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route('/get_benchmark_status')
def get_benchmark_status():
    resp = make_response(json.dumps(data_handler.get_benchmark_status('admin')))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/repeat_benchmark')
def repeat_benchmark():
    resp = make_response(json.dumps(data_handler.repeat_benchmark('admin')))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/start_bench_th')
def start_bench_thread():
    resp = make_response(json.dumps(start_bench_(config)))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/hosts_aggregation_cpu')
def hosts_aggregation():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)
    
    resp = make_response(data_handler.hosts_aggregation_cpu(timestamp_begin, timestamp_end))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/hosts_aggregation_memory')
def hosts_aggregation_memory():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(data_handler.hosts_aggregation_memory(timestamp_begin, timestamp_end))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/hosts_aggregation_disk')
def hosts_aggregation_disk():
    timestamp_begin = request.args.get('timestamp_begin', None)
    timestamp_end = request.args.get('timestamp_end', None)

    resp = make_response(data_handler.hosts_aggregation_disk(timestamp_begin, timestamp_end))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/vcpus_for_aggregate')
def vcpus_for_aggregate():
    project = request.args.get('project')
    resp = make_response(data_handler.vcpus_for_aggregate(project))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route('/hosts_aggregates')
def hosts_aggregates():
    resp = make_response(json.dumps(data_handler.host_aggregates('admin')))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

if __name__ == '__main__':
    worker = threading.Thread(target=store_host_data, kwargs={'hosts' : HOSTS, 'config' : config})
    worker.daemon = False
    worker.start()
    
    app.debug = True
    app.run(host='0.0.0.0', port=10090)

