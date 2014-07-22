import json
import numpy

class Reduction:
    def points_reduction(self, old_data, key):
        scale = len(old_data)/100 + 1
        if scale <= 4:
            return old_data
        local=0
        local2=scale/2
        new_points = []
        for c in range(0,len(old_data),scale):

            if (local+scale) <= len(old_data)-1:
                final = local+local2
            else:
                final = len(old_data)-2
            window = []
            for d in range(local, final):
                window.append(old_data[d][key])
            mean_value = numpy.mean(window)
            data_dict = {}
            data_dict['timestamp'] = old_data[final]['timestamp']
            data_dict[key] = mean_value
            new_points.append(data_dict)
            local+=scale
    
        return new_points
    
    def points_reduction_for_percent(self, old_data, key):
        scale = len(old_data)/100 + 1
        if scale <=4:
            return old_data
        local=0
        local2=scale/2
        new_points = []
        for c in range(0,len(old_data),scale):
            if(local+scale) <= len(old_data):
                final = local+local2
            else:
                final = len(old_data)-1
            window = []
            for d in range(local, final):
                window.append(json.loads(old_data[d]['data'])[0]['percent'])

            mean_value = numpy.mean(window)
            data_dict = {}
            data_dict['timestamp'] = old_data[final]['timestamp']
            data_dict[key] = json.dumps([{'percent': mean_value}])
            new_points.append(data_dict)
            local+=scale
    
    
        return new_points
    
    
    def points_reduction_disk(self, old_data):
        scale = len(old_data)/200 + 1
        if scale <= 4:
            return old_data
        local = 0
        local2 = scale/2
        newpoints = []
        for c in range(0,len(old_data),scale):
            if (local+scale) <= len(old_data):
                final = local+local2
            else:
                final = len(old_data)-1
            
            dic = {}
            if (local+scale) <= len(old_data):
                for d in range(local,final):
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
                local += scale
        return newpoints

