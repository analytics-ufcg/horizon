from host_data import HostDataHandler

import time, datetime


class HostMetricsCalculator:

    def get_host_availability_metrics(self, timestamp_begin, timestamp_end):
        import numpy


        hour = 3600.0
        host_handler = HostDataHandler()

        db_lines = host_handler.get_data_db('HostStatus', timestamp_begin, timestamp_end)
        host_data = db_lines[0]['data']
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
                begin_time_down = last_time_down
                beginning_down_flag = True
                beginning_up_flag = False
                time_up = (last_time_up - begin_time_down).total_seconds()

                list_ups_time.append(time_up)
            else:
                continue

        mtbf = ((sum(list_ups_time) / len(list_downs_time))) / hour

        result['MTBF'] = "%.3f hours" % mtbf
        result['MTTF'] = "%.3f hours" % (((period_total - (sum(list_ups_time))) / len(list_downs_time)) / hour)
        result['Max time up'] = "%.3f hours" %  (max(list_ups_time) / hour)
        result['Max time down'] = "%.3f hours" %   (max(list_downs_time) / hour)

        ups = numpy.array(list_ups_time)
        downs = numpy.array(list_downs_time)

        result['Average time up'] = "%.3f hours" % (list_ups_time.mean() / hour)
        result['Average time down'] = "%.3f hours" % (list_downs_time.mean() / hour)
        result['Deviation Up'] = "%.3f hours" % (list_ups_time.std() / hour)
        result['Deviation Down'] = "%.3f hours" % (list_downs_time.std() / hour)
        print result
        return result


        
 
    




