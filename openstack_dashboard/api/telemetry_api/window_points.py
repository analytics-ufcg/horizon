from telemetry_data import DataHandler
import json
import numpy

def points_reduction(old_data,key):
    scale = len(old_data)/300 + 1
    if scale <= 4:
        return old_data
    local=0
    local2=scale/2
    new_points = []
    for c in range(0,len(old_data),scale):
        if(local+scale) <= len(old_data):
            window = []
            for d in range(local, local+scale):
                window.append(old_data[d][key])
            mean_value = numpy.mean(window)


            data_dict = {}
            data_dict['timestamp'] = old_data[local]['timestamp']
            data_dict[key] = mean_value
            new_points.append(data_dict)

            local+=scale

        elif(local <= len(old_data)):
            window = []
            for d in range(local, len(old_data)):
                window.append(old_data[d][key])
            mean_value = numpy.mean(window)

            data_dict = {}
            data_dict['timestamp'] = old_data[local]['timestamp']
            data_dict[key] = mean_value
            new_points.append(data_dict)
            
            local+=scale

    return new_points

def points_reduction_for_percent(old_data, key):
    scale = len(old_data)/300 + 1
    if scale <=4:
        return old_data
    local=0
    local2=scale/2
    new_points = []
    for c in range(0,len(old_data),scale):
        if(local+scale) <= len(old_data):
            window = []
            for d in range(local, local+scale):
                window.append(json.loads(old_data[d]['data'])[0]['percent'])
            mean_value = numpy.mean(window)


            data_dict = {}
            data_dict['timestamp'] = old_data[local+local2/2]['timestamp']
            data_dict[key] = json.dumps([{'percent': mean_value}])
            new_points.append(data_dict)

            local+=scale

        elif(local <= len(old_data)):
            window = []
            for d in range(local, len(old_data)):
                window.append(json.loads(old_data[d]['data'])[0]['percent'])
            mean_value = numpy.mean(window)


            data_dict = {}
            data_dict['timestamp'] = old_data[len(old_data)-1]['timestamp']
            data_dict[key] = json.dumps([{'percent': mean_value}])
            new_points.append(data_dict)
            local+=scale

    return new_points


def points_reduction_by_server_cpu(timestamp_begin, timestamp_end, hosts):
    data_handler = DataHandler()
    data = []
    old_data = data_handler.hosts_cpu(timestamp_begin, timestamp_end)
    key = 'data'
    for host in range(len(hosts)):
        dict_host = {}
        dict_host["host_address"] = hosts[host]
        dict_host['data'] = points_reduction(old_data[host]['data'],key)
        data.append(dict_host)
    return data

def points_reduction_by_server_memory(timestamp_begin, timestamp_end, hosts):
    data_handler = DataHandler()
    data = []
    old_data = data_handler.hosts_memory(timestamp_begin, timestamp_end)
    key = 'data'
    for host in range(len(hosts)):
        dict_host = {}
        dict_host["host_address"] = hosts[host]
        dict_host['data'] = points_reduction_for_percent(old_data[host]['data'],key)
        print dict_host['data']
        data.append(dict_host)
    return data

def points_reduction_by_server_disk(timestamp_begin, timestamp_end, hosts):
    data_handler = DataHandler()
    data = []
    old_data = data_handler.hosts_disk(timestamp_begin, timestamp_end)
    for host in range(len(hosts)):
        dict_host = {}
        dict_host["host_address"] = hosts[host]
        dict_host['data'] = points_reduction_disk(old_data[host]['data'])
        data.append(dict_host)
    return data


def points_reduction_vm(timestamp_begin,timestamp_end,resource_id):
    dh = DataHandler()
    old_data = json.loads(dh.cpu_util_from(timestamp_begin,timestamp_end,resource_id))
    key2 = "cpu_util_percent"
    data  =  points_reduction(old_data,key2)
    return data

def points_reduction_disk(old_data):
    scale = len(old_data)/300 + 1
    if scale <= 4:
        return old_data
    local = 0
    local2 = scale/2
    newpoints = []
    for c in range(0,len(old_data),scale):
        dic = {}
        if (local+scale) <= len(old_data):
            for d in range(local,local+scale):
                valores = json.loads(old_data[d]['data'])
                for v in valores:
                    if( v['device'] in dic):
                        dic[v['device']].append(v['percent'])
                    else:
                        dic[v['device']] = []
                        dic[v['device']].append(v['percent'])
            lista_mean = []
            for chave in dic.keys():
                mean = {"device":chave,"percent":numpy.mean(dic[chave])}
                lista_mean.append(mean)
            data_dict = {}
            data_dict['timestamp'] = old_data[local]['timestamp']
            data_dict['data'] = json.dumps(lista_mean)
            newpoints.append(data_dict)
            newpoints.append(data_dict)
            local += scale
        elif(local <= len(old_data)):
             for d in range(local,len(old_data)):
                 valores = json.loads(old_data[d]['data'])
                 for k in valores:
                     if( k['device'] in dic):
                         dic[k['device']].append(k['percent'])
                     else:
                         dic[k['device']] = []
                         dic[k['device']].append(k['percent'])
             lista_mean = []
             for chave in dic.keys():
                 mean = {"device":chave,"percent":numpy.mean(dic[chave])}
                 lista_mean.append(mean)
             data_dict = {}
             data_dict['timestamp'] = old_data[-1]['timestamp']
             data_dict['data'] = json.dumps(lista_mean)
             newpoints.append(data_dict)
             local += scale
    return newpoints
