import ConfigParser

#Singleton Class
class ConfigManager():

    _instance = None

    class Singleton:
        config_parser = None
        config_path='openstack_dashboard/api/telemetry_api/environment.conf'

        def __init__(self):
            self.config_parser = ConfigParser.ConfigParser()
            self.config_parser.read(self.config_path)

    def __init__(self):
        if ConfigManager._instance is None:
            ConfigManager._instance = ConfigManager.Singleton()
            
        self._EventHandler_instance = ConfigManager._instance   

    def __getattr__(self, aAttr):
        return getattr(self._instance, aAttr)

    def get_db_server(self):
        return self._instance.config_parser.get('Misc', 'dbserver')

    def get_db_user(self):
        return self._instance.config_parser.get('Misc', 'dbuser')

    def get_db_pass(self):
        return self._instance.config_parser.get('Misc', 'dbpass')

    def get_host_db_name(self):
        return self._instance.config_parser.get('Misc', 'HostsDbName')

    def get_host_db_table(self):
        return self._instance.config_parser.get('Misc', 'HostsDbTable')

    def get_admin_user(self):
        return self._instance.config_parser.get('Openstack', 'OSUsername')

    def get_admin_pass(self):
        return self._instance.config_parser.get('Openstack', 'OSPassword')

    def get_admin_tenant_id(self):
        return self._instance.config_parser.get('Misc', 'AlarmPostUrl')

    def get_oauth_url(self):
        return self._instance.config_parser.get('Openstack', 'OSAuthUrl')

    def get_alarm_url(self):
        return self._instance.config_parser.get('Misc', 'AlarmPostUrl')

    def get_benchmark_db(self):
        return self._instance.config_parser.get('Benchmark', 'DbBenchmark')

    def get_benchmark_table(self):
        return self._instance.config_parser.get('Benchmark', 'BenchmarkTable')

