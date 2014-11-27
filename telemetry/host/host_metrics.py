from host_data import HostDataHandler

import time, datetime
import numpy

class HostMetricResult:

    def __init__(self, host, mtbf, mttf, max_time_up, avg_time_up, std_time_up, availability_percent):
        self.host = host
        self.mtbf = mtbf
        self.mttf = mttf
        self.max_time_up = max_time_up
        self.avg_time_up = avg_time_up
        self.std_time_up = std_time_up
        self.availability_percent = availability_percent


class HostMetricsCalculator:

    def _get_availability_metrics_per_host(self, host_data, total_period):
        # init variables
        hour = 3600.0
        result = {}
        list_ups_time = []
        list_downs_time = []
        beginning_up_flag = False
        beginning_down_flag = False
        last_time_up = 0
        begin_time_up = 0
        begin_time_down = 0
        last_time_down = 0

        host_status = host_data['data']

        # loop over data
        for i in range(len(host_status)):
            if host_status[i]['data'] == 'T' and not beginning_up_flag:
                begin_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                beginning_up_flag = True
                if beginning_down_flag:
                    last_time_down = begin_time_up
                    time_down = (last_time_down - begin_time_down).total_seconds()
                    list_downs_time.append(time_down)
            elif host_status[i]['data'] == 'F' and beginning_up_flag:
                last_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                begin_time_down = last_time_up
                beginning_down_flag = True
                beginning_up_flag = False
                time_up = (last_time_up - begin_time_up).total_seconds()

                list_ups_time.append(time_up)
            elif i == len(host_status) - 1:
                if host_status[i]['data'] == 'T' and beginning_up_flag:
                    last_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                    time_up = (last_time_up - begin_time_up).total_seconds()
                    list_ups_time.append(time_up)
                else:
                    begin_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                    last_time_down = begin_time_up
                    time_down = (last_time_down - begin_time_down).total_seconds()
                    list_downs_time.append(time_down)

            else:
                continue

        # calculate metrics 
        if not list_downs_time:
           mtbf = float("inf")
           mttf = float("inf")
           mttr = float("inf")
           max_time_up = total_period
           avg_time_up = total_period
           std_time_up = 0
           availability_percent = 1
           availability_metrics = ("NaN")
        else:
           total_up_time = sum(list_ups_time)
           total_up_time_without_first = sum(list_ups_time[1:]) 
           total_down_time = sum(list_downs_time)
           failures_count = len(list_downs_time)
           mtbf = (total_up_time / failures_count) / hour
           mtbf_without_first =  (total_up_time_without_first / failures_count) / hour
           mttf = (total_period / failures_count) / hour
           list_ups_time = numpy.array(list_ups_time)
           list_downs_time = numpy.array(list_downs_time)
            
           mttr = (total_down_time / failures_count) / hour          
           availability_metrics = (mtbf / (mtbf + mttr) * 100)


           max_time_up = (max(list_ups_time) / hour)
           avg_time_up = (list_ups_time.mean() / hour)
           std_time_up = (list_ups_time.std() / hour)
           availability_percent = total_up_time / (total_period * hour)


        # create result obj 
        metric_result_obj = HostMetricResult(host_data['host_address'],
            mtbf, mttf,
            max_time_up, avg_time_up, std_time_up, availability_percent)

        return metric_result_obj

    def get_host_availability_metrics(self, timestamp_begin, timestamp_end):
        hour = 3600.0

        #print '---------'
        #print timestamp_begin

        # get host data from db
        host_handler = HostDataHandler()
        db_lines = host_handler.get_data_db('HostStatus', timestamp_begin, timestamp_end)

        # format timestamps
        time_begin = datetime.datetime.strptime(timestamp_begin, '%Y-%m-%dT%H:%M:%S')
        time_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')
        total_period = ((time_end - time_begin).total_seconds()) / hour

        # calculte
        results = []

        for host_data in db_lines:
            timestamp = host_handler.get_last_failure(timestamp_begin, host_data['host_address'])
            if timestamp is not None:
                time_begin = datetime.datetime.strptime(timestamp_begin, '%Y-%m-%dT%H:%M:%S')
                time_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')
                total_period = ((time_end - time_begin).total_seconds()) / hour
                        
            metric_result_obj = self._get_availability_metrics_per_host(host_data, total_period)
            results.append(metric_result_obj)

        return results


