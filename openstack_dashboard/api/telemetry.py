class RecommendationsUpgrade:

    def __init__(self,host,cpu_total,cpu_usage,cpu_p, mem_total, mem_usage, mem_p, disk_total, disk_usage, disk_p):
        self.host = host
        self.cpu_total = cpu_total
        self.cpu_usage = cpu_usage
        self.cpu_percentage = cpu_p
        self.memory_total = mem_total
        self.memory_usage = mem_usage
        self.memory_percentage = mem_p
        self.disk_total = disk_total
        self.disk_usage = disk_usage
        self.disk_percentage = disk_p

class AlarmsList:

    def __init__(self, alarm_id, alarm_name, enabled, description):
        self.alarm_id = alarm_id
        self.alarm_name = alarm_name
        self.enabled = enabled
        self.description = description

class AlarmsHistory:

    def __init__(self, timestamp, alarm_name, alarm_type, detail):
        self.timestamp = timestamp
        self.alarm_name = alarm_name
        self.alarm_type = alarm_type
        self.detail = detail
    
class RecommendationFlavors:
    
    def __init__(self, name, sugestion, lose, violations):
        self.name = name
        self.sugestion = sugestion
        self.lose = lose
        self.violations = violations    
    

class RecommendataionPowerStatus:

    def __init__(self, host, status):
        self.host = host
        self.status = status

class RecommendationMigration:

    def __init__(self, host,server, endhost):
       self.host = host
       self.server = server
       self.endhost = endhost


class BenchmarkDisk:

    def __init__(self,host,avg,median,min,max,first,second,third,fourth):
        self.host = host
        self.avg = avg
        self.median = median
        self.min = min
        self.max = max
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


class BenchmarkCpu:

    def __init__(self,host,avg,median,min,max,first,second,third,fourth):
        self.host = host
        self.avg = avg
        self.median = median
        self.min = min
        self.max = max
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth

class BenchmarkMemory:

    def __init__(self,host,avg,median,min,max,first,second,third,fourth):
        self.host = host
        self.avg = avg
        self.median = median
        self.min = min
        self.max = max
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
 
