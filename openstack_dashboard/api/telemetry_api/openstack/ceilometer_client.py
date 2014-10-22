import ast
from keystone_client import KeystoneClient

from ceilometerclient import client

class CeilometerClient:

    def __init__(self, config):
        ceilometer_api_version = config.get('Openstack', 'ceilometerapiversion')
        username = config.get('Openstack', 'osusername')
        password = config.get('Openstack', 'ospassword')
        tenant_admin = config.get('Openstack', 'ostenantadmin')
        auth_url = config.get('Openstack', 'osauthurl')
        self.__alarm_url = config.get('Misc', 'alarmposturl')
        self.ceilometer = client.get_client(ceilometer_api_version, os_username=username, os_password=password, os_tenant_name=tenant_admin, os_auth_url=auth_url)

    def __build_query(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        query = []

        if any([timestamp_begin, timestamp_end, resource_id, project_id]):
            if timestamp_begin:
                query.append({'field':'timestamp', 'op':'gt', 'value':timestamp_begin})

            if timestamp_end:
                query.append({'field':'timestamp', 'op':'lt', 'value':timestamp_end})

            if resource_id:
                query.append({'field':'resource_id', 'op':'eq', 'value': resource_id})

            if project_id:
                query.append({'field':'project_id', 'op':'eq', 'value':project_id})

        return query

    def __get_cpu_util_raw(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        query = self.__build_query(timestamp_begin, timestamp_end, resource_id, project_id)

        return self.ceilometer.samples.list('cpu_util', query)

    def get_cpu_util(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        data = self.__get_cpu_util_raw(timestamp_begin, timestamp_end, resource_id, project_id)
        ret = []
        for d in data:
            ret.append({ 'resource_id' : d.resource_id, 'timestamp' : d.timestamp, 'cpu_util_percent' : d.counter_volume })
    
        return ret

    def get_cpu_util_flavors(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        data = self.__get_cpu_util_raw(timestamp_begin, timestamp_end, resource_id, project_id)
        ret = []
        for d in data:
            ret.append({'VM': d.resource_id, 'Cores': d.resource_metadata['flavor.vcpus'], 'CPU_UTIL': d.counter_volume})
        return ret

    def __get_network_incoming_bytes_rate_raw(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        query = self.__build_query(timestamp_begin, timestamp_end, resource_id, project_id)

        return self.ceilometer.samples.list('network.incoming.bytes.rate', query)

    def __get_network_outgoing_bytes_rate_raw(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        query = self.__build_query(timestamp_begin, timestamp_end, resource_id, project_id)

        return self.ceilometer.samples.list('network.outgoing.bytes.rate', query)

    def get_network_incoming_bytes_rate(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        #TODO: resource_id is unique for each interface, currently can't query data for a single instance by resource_id.
        data = self.__get_network_incoming_bytes_rate_raw(timestamp_begin, timestamp_end, None, project_id)
        ret = []

        for d in data:
            if str(resource_id) in d.resource_metadata['instance_id']:
                ret.append({'resource_id': d.resource_metadata['instance_id'], 'timestamp': d.timestamp, 'network_incoming_bytes_rate': d.counter_volume })

        return ret

    def get_network_outgoing_bytes_rate(self, timestamp_begin=None, timestamp_end=None, resource_id=None, project_id=None):
        #TODO: resource_id is unique for each interface, currently can't query data for a single instance by resource_id.
        data = self.__get_network_outgoing_bytes_rate_raw(timestamp_begin, timestamp_end, None, project_id)
        ret = []

        for d in data:
            if str(resource_id) in d.resource_metadata['instance_id']:
                ret.append({'resource_id': d.resource_metadata['instance_id'], 'timestamp': d.timestamp, 'network_outgoing_bytes_rate': d.counter_volume })

        return ret

    def set_alarm(self, name, meter, threshold, operator, period, evaluation_period, send_mail, email_admin, instance=""):
        try:
            print email_admin
            alarm = ""
            stringE = "user-%s admin-%s" % (str(send_mail),str(email_admin))
            if(instance == ""):
                alarm = self.ceilometer.alarms.create(name=name, type='threshold', meter_name=meter, threshold=threshold, comparison_operator=operator, statistic='avg', period=period, evaluation_periods=evaluation_period, repeat_actions=True, alarm_actions=[self.__alarm_url, stringE, 'log:/'])

            else:
                alarm = self.ceilometer.alarms.create(name=name, type='threshold', meter_name=meter, threshold=threshold, matching_metadata={'resource_id': instance}, comparison_operator=operator, statistic='avg', period=period, evaluation_period=evaluation_period, repeat_action=True, alarm_actions=[self.__alarm_url, stringE, 'log:/'])

         #   print alarm.alarm_actions
            return True
        except:
            return None


    def get_alarms_history(self, timestamp_begin=None, timestamp_end=None):
        query = []
        
        if any([timestamp_begin, timestamp_end]):
            if timestamp_begin:
                query.append({'field':'timestamp', 'op':'gt', 'value':timestamp_begin})

            if timestamp_end:
                query.append({'field':'timestamp', 'op':'lt', 'value':timestamp_end})

        alarms = self.ceilometer.alarms.list()

        ret = []
        for alarm in alarms:
            resource_id = self.get_alarm_resourceId(alarm)

            ret.append({ 'alarm_name':alarm.name, 'alarm_id':alarm.alarm_id, 'history':[event.__dict__['_info'] for event in self.ceilometer.alarms.get_history(alarm.alarm_id, query)], 'resource_id': resource_id })

        return ret

    def get_alarm_resourceId(self, alarm):
        for query in alarm.threshold_rule['query']:
            return query['value']

    def get_alarm_userid(self, alarm_id):
        alarm = str(self.ceilometer.alarms.get(alarm_id))[7:-1]
        return ast.literal_eval(alarm)['user_id']

    def get_alarm_projectid(self, alarm_id):
        alarm = str(self.ceilometer.alarms.get(alarm_id))[7:-1]
        return ast.literal_eval(alarm)['project_id']

    def get_alarm_parameters(self):
        alarms = self.ceilometer.alarms.list()
        parametros = {}
        for alarm in alarms:
            parametros[alarm.alarm_id] = [alarm.name, alarm.enabled, alarm.description]
        return parametros


    def get_alarm_email_status(self, alarm_id):
        alarm = self.ceilometer.alarms.get(alarm_id)
        try:
            return alarm.alarm_actions[1]
        except:
            return None


    def delete_alarms(self, alarm_id):
        self.ceilometer.alarms.delete(alarm_id)
        return 'removido com sucesso'

