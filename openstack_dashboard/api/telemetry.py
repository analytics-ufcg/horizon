# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 B1 Systems GmbH
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class RecommendationUpgrade:

    def __init__(self, host,
                 cpu_total, cpu_usage,
                 cpu_p, mem_total,
                 mem_usage, mem_p,
                 disk_total, disk_usage,
                 disk_p):
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


class RecommendationPowerStatus:

    def __init__(self, host, status):
        self.host = host
        self.status = status


class RecommendationMigration:

    def __init__(self, host, server, name, endhost, project):
        self.host = host
        self.server = server
        self.name = name
        self.endhost = endhost
        self.project = project


class BenchmarkDisk:

    def __init__(self, host, avg,
                 median, min, max,
                 first, second, third, fourth):
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

    def __init__(self, host, avg,
                 median, min, max,
                 first, second, third, fourth):
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

    def __init__(self, host, avg,
                 median, min, max,
                 first, second, third, fourth):
        self.host = host
        self.avg = avg
        self.median = median
        self.min = min
        self.max = max
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


class UserMessages:

    def __init__(self, id, sender,
                 subject, timestamp,
                 message, read):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.timestamp = timestamp
        self.message = message
        self.read = read


class HostMessages:

    def __init__(self, id, zone):
        self.id = id
        self.zone = zone