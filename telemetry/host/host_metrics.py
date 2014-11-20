from host_data import HostDataHandler

import time, datetime


class HostMetricsCalculator:

    def __init__(self):

        self.MTBF = ""
        self.MTTF = ""
        self.max_time_up = "" 
        self.max_time_down = ""
        self.average_time_up = ""
        self.average_time_down = ""
        self.deviation_up = ""
        self.deviation_down = ""


    def get_host_availability_metrics(self, timestamp_begin, timestamp_end):
        import numpy


        hour = 3600.0
        host_handler = HostDataHandler()

        db_lines = host_handler.get_data_db('HostStatus', timestamp_begin, timestamp_end)
        host_data = db_lines[0]['data']
        print host_data
        time_begin = datetime.datetime.strptime(timestamp_begin, '%Y-%m-%dT%H:%M:%S')
        time_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')
        period_total = ((time_end - time_begin).total_seconds()) / hour     


        result = {}
        list_ups_time = []
        list_downs_time = []
        beginning_up_flag = False
        beginning_down_flag = False
        last_time_up = 0
        begin_time_up = 0

        begin_time_down = 0
        last_time_down = 0
        for i in range(len(host_data)):
            if host_data[i]['data'] == 'T' and not beginning_up_flag:
                begin_time_up = datetime.datetime.strptime(host_data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                beginning_up_flag = True
                if beginning_down_flag:
                    last_time_down = begin_time_up
                    time_down = (last_time_down - begin_time_down).total_seconds()
                    list_downs_time.append(time_down)
            elif host_data[i]['data'] == 'F' and beginning_up_flag:
                last_time_up = datetime.datetime.strptime(host_data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                begin_time_down = last_time_up
                beginning_down_flag = True
                beginning_up_flag = False
                time_up = (last_time_up - begin_time_up).total_seconds()
                
                list_ups_time.append(time_up)
            elif i == len(host_data) - 1:
                if host_data[i]['data'] == 'T' and beginning_up_flag:
                    last_time_up = datetime.datetime.strptime(host_data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                    time_up = (last_time_up - begin_time_up).total_seconds()
                    list_ups_time.append(time_up)
                else:
                    begin_time_up = datetime.datetime.strptime(host_data[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                    last_time_down = begin_time_up
                    time_down = (last_time_down - begin_time_down).total_seconds()
                    list_downs_time.append(time_down)
  
            else:
                continue

        try:
            mtbf = ((sum(list_ups_time) / len(list_downs_time))) / hour
            mttf = ((period_total - (sum(list_ups_time))) / len(list_downs_time)) / hour

        except Exception, e:
            print e                  
            mtbf = 1
            mttf = 0

        print list_ups_time

        if list_ups_time == [] : list_ups_time = [0]
        if list_downs_time == [] : list_downs_time = [0]


        result['MTBF'] = "%.3f hours" % mtbf
        result['MTTF'] = "%.3f hours" % mttf
        result['Max time up'] = "%.3f hours" %  (max(list_ups_time) / hour)
        result['Max time down'] = "%.3f hours" %   (max(list_downs_time) / hour)

        list_ups_time = numpy.array(list_ups_time)
        list_downs_time = numpy.array(list_downs_time)

        result['Average time up'] = "%.3f hours" % (list_ups_time.mean() / hour)
        result['Average time down'] = "%.3f hours" % (list_downs_time.mean() / hour)
        result['Deviation Up'] = "%.3f hours" % (list_ups_time.std() / hour)
        result['Deviation Down'] = "%.3f hours" % (list_downs_time.std() / hour)
       
        print result
        

        # Valores atribuidos para as variaveis da classe 
        # Mas ainda retorna um dicionario com todas as metricas

             
        self.MTBF = result['MTBF']
        self.MTTF = result['MTTF']
        self.max_time_up = result['Max time up'] 
        self.max_time_down = result['Max time down']
        self.average_time_up = result['Average time up']
        self.average_time_down = result['Average time down']  
        self.deviation_up = result['Deviation Up']
        self.deviation_down = result['Deviation Down'] 


        return result


 

        
    
    




