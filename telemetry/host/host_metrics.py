from host_data import HostDataHandler
from collections import OrderedDict

from collections import OrderedDict
import time, datetime
import time, datetime, json
import numpy

class HostMetricResult:

    def __init__(self, host, mtbf, mttr, total_up_time, total_down_time, failures_count, availability_percent, begin_time):
        self.host = host
        self.mtbf = mtbf
        self.mttr = mttr
        self.total_up_time = total_up_time
        self.total_down_time = total_down_time
        self.failures_count = failures_count
        self.availability_percent = availability_percent
        self.begin_time = begin_time

    def to_dict(self):
        obj_to_dict = {'$row': self.host, 'MTBF': self.mtbf , 'MTTR': self.mttr, 'Failure': self.failures_count }
        return obj_to_dict

class HostMetricsCalculator:

    def _get_availability_metrics_per_host(self,host_ip, host_data, time_begin, total_period):
        # init variables
        hour = 3600.0
        result = {}
        list_ups_time = []
        list_downs_time = []
        total_up_time = 0
        total_down_time = 0
        failures_count = 0
        beginning_up_flag = False
        beginning_down_flag = False
        last_time_up = 0
        begin_time_up = 0
        begin_time_down = 0
        last_time_down = 0
        availability_percent = 100
        host_status = host_data['data']

        # loop over data
        for i in range(len(host_status)):
            if host_status[i]['status'] == 'T' and not beginning_up_flag:
                begin_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                beginning_up_flag = True
                if beginning_down_flag:
                    last_time_down = begin_time_up
                    time_down = (last_time_down - begin_time_down).total_seconds()
                    list_downs_time.append(time_down)
            elif host_status[i]['status'] == 'F' and beginning_up_flag:
                last_time_up = datetime.datetime.strptime(host_status[i]['timestamp'], '%Y-%m-%dT%H:%M:%S')
                begin_time_down = last_time_up
                beginning_down_flag = True
                beginning_up_flag = False
                time_up = (last_time_up - begin_time_up).total_seconds()

                list_ups_time.append(time_up)
            elif i == len(host_status) - 1:
                if host_status[i]['status'] == 'T' and beginning_up_flag:
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
        total_up_time = sum(list_ups_time)
        total_up_time_without_first = sum(list_ups_time[1:])
        total_down_time = sum(list_downs_time)
        failures_count = len(list_downs_time)

        if not list_downs_time:
           mtbf = '-'
           mttf = '-'
           mttr = "-"
           max_time_up = total_period / hour
           avg_time_up = total_period / hour
           std_time_up = 0
           availability_percent = 100
           availability_metrics = float("NaN")
        else:
           list_ups_time = numpy.array(list_ups_time)
           list_downs_time = numpy.array(list_downs_time)

           mtbf = (total_up_time / failures_count) / hour
           mtbf = round(mtbf, 2)
           mtbf_without_first =  (total_up_time_without_first / failures_count) / hour
           mttf = (total_period / failures_count) / hour
           mttr = (total_down_time / failures_count) / hour          
           mttr = round(mttr, 2)

           availability_metrics = (mtbf / (mtbf + mttr)) * 100

           max_time_up = (max(list_ups_time) / hour)
           avg_time_up = (list_ups_time.mean() / hour)
           std_time_up = (list_ups_time.std() / hour)
           availability_percent = (total_up_time / total_period) * 100

        # create result obj 
        metric_result_obj = HostMetricResult(host_ip,
            mtbf, mttr,
            round(total_up_time/hour, 2),
            round(total_down_time/hour, 2),
            failures_count,
            round(availability_percent, 2), 
            time_begin)

        return metric_result_obj

    def get_host_availability_metrics(self, timestamp_begin, timestamp_end):
        hour = 3600.0

        # get host data from db
        host_handler = HostDataHandler()

        # calculte
        results = []
        host_obj_list = host_handler.get_hosts()

        print '====='
        for i in range(len(host_obj_list)):
            #get host last failure
            host_ip = host_obj_list[i].get_ip()
            last_failure_timestamp = host_handler.get_last_failure(timestamp_begin, host_ip)

            #reset to initial parameters
            time_begin = datetime.datetime.strptime(timestamp_begin, '%Y-%m-%dT%H:%M:%S')
            time_end = datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S')
            total_period = (time_end - time_begin).total_seconds()
            timestamp_begin_host = timestamp_begin
            
            #update begin_time and total_period to include failure
            if last_failure_timestamp is not None:
                time_begin = datetime.datetime.strptime(last_failure_timestamp, '%Y-%m-%dT%H:%M:%S')
                total_period = (time_end - time_begin).total_seconds()
                timestamp_begin_host = last_failure_timestamp
           
            host_data = host_handler.get_host_status_db(host_ip, timestamp_begin_host, timestamp_end)
            metric_result_obj = self._get_availability_metrics_per_host(host_ip, host_data, time_begin, total_period)
            results.append(metric_result_obj)
            
        return results
