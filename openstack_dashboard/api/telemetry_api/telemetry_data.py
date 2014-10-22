from openstack.ceilometer_client import CeilometerClient
from openstack.keystone_client import KeystoneClient
from openstack.nova_client import NovaClient
from host_data import HostDataHandler
from benchmark_data import BenchmarkDataHandler
from reduction import Reduction

import json, ast, smtplib, math, requests, numpy, ast, ConfigParser

import analytics.recommendations

def send_email(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


class MigrateException(Exception):
    
    def __init__(self,error,message):
        Exception.__init__(self)
        self.error = error
        self.message = message
class DataHandler:

    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        self.__config.read('openstack_dashboard/api/telemetry_api/environment.conf')
        self.__ceilometer = CeilometerClient(self.__config)
        self.__keystone = KeystoneClient(self.__config)
        self.__nova = NovaClient(self.__config)
        server = self.__config.get('Misc', 'dbserver')
        user = self.__config.get('Misc', 'dbuser')
        passwd = self.__config.get('Misc', 'dbpass')
        database = self.__config.get('Misc', 'hostsdbname')
        table = self.__config.get('Misc', 'hostsdbtable')
        self.__hosts_db = HostDataHandler(server, user, passwd, database, table)
        self.__benchmark_db = BenchmarkDataHandler(server, user, passwd)
        self.__reduction = Reduction()

    def get_config(self):
        return self.__config

    def projects(self):
        return json.dumps(self.__keystone.projects)

    def get_critical_hosts(self,instances_critical, information):
        critical_hosts = []
        for cpn in information:
            cpn_name = cpn.keys()[0]
            cpn_server_list = cpn[cpn_name]['vms'].keys()
            for server in cpn_server_list:
                if server in instances_critical:
                    critical_hosts.append(cpn_name)
        return critical_hosts

    def suggestion(self, list_not_ignore=[]):
        project_list = [ project['name'] for project in json.loads(self.projects())] #returns the list of existing projects
        compute_nodes_info_list = self.__nova.vm_info(project_list) #list of jsons - json correspond to a compute node information
        instances_id_project = {} #dict instances_id : project_name
        for compute_node_aux in compute_nodes_info_list:
            try:
                compute_name = compute_node_aux.keys()[0] #get the name of compute node to access information
                for key in compute_node_aux[compute_name]['Info_project'].keys(): #key represent a project
                    #id represent de id of any instance present in a given project(key) and in the compute_name
                    for id in compute_node_aux[compute_name]['Info_project'][key]:
                        instances_id_project[id] = key
            except Exception as excp:
                return {"error": excp.message}
        #get the list of critical instances (can't migrate them)
        critical_instances = self.__nova.critical_instances(project_list)
        #list of critical hosts
        critical_cpn = self.get_critical_hosts(critical_instances,compute_nodes_info_list)
        shutdown = {} #dict compute_node : True/False for shutdown
        migrations = {} #dict with all migrations 
        compute_nodes_copy = compute_nodes_info_list[:] #copy to aux with the algorithm
        owner_cpn_instance = {}
        #for cp in compute_nodes_info_list:
        #    owner_cpn = cp.keys()[0]
        #    vms_cp = cp[owner_cpn]['vms'].keys()
        #    for v in vms_cp:
        #        owner_cpn_instance[v] = owner_cpn
        #begin of algorithm
        #cpn_data - compute node data
        try:
            for cpn_data in compute_nodes_info_list:
                data  = cpn_data.copy() #contains all information about a compute node
                actual_cpn = cpn_data.keys()[0] #actual compute node (try migration for all instances)
                #verify is the compute node has critical instances
                if actual_cpn not in critical_cpn:
                    if( len( data[actual_cpn]['vms'].keys()) > 0 ):
                        instances_data = data[actual_cpn]['vms'].copy() #copy the list of vms
                        compute_nodes_copy.remove(cpn_data) #remove all data from compute node in the copy
                        migration_flag = False #flag to say if the instace can migrate to other compute node
                        migrations[actual_cpn] = {} #dict with all migrations for compute node
                        for instance_id in instances_data:
                            for other_cpn in compute_nodes_copy:
                                #verification - instance is not critical
                                if (other_cpn not in critical_cpn and instance_id not in critical_instances):
                                    migration_flag = False
                                    other_cpn_name = other_cpn.keys()[0]
                                    if list_not_ignore == [] or actual_cpn in list_not_ignore:
                                        if(other_cpn[other_cpn_name]['Livre'][0] >= instances_data[instance_id][0] and
                                           other_cpn[other_cpn_name]['Livre'][1] >= instances_data[instance_id][1] and
                                           other_cpn[other_cpn_name]['Livre'][2] >= instances_data[instance_id][2]):
                                           from_cpn = None
                                           migrate_to_cpn = None
                                           if instance_id in owner_cpn_instance:
                                               from_cpn = owner_cpn_instance[instance_id].keys()[0]
                                               migrate_to_cpn = owner_cpn_instance[instance_id][from_cpn]
                                           else:
                                               from_cpn = actual_cpn
                                               migrate_to_cpn = other_cpn_name
                                           if actual_cpn == from_cpn or actual_cpn == migrate_to_cpn:
                                               #update values of free resources
                                               new_values = [other_cpn[other_cpn_name]['Livre'][0] - instances_data[instance_id][0],
                                                         other_cpn[other_cpn_name]['Livre'][1] - instances_data[instance_id][1],
                                                         other_cpn[other_cpn_name]['Livre'][2] - instances_data[instance_id][2]]
                                               other_cpn[other_cpn_name]['Livre'] = new_values
                                               #sending instance to the other host with all information
                                               instances_other_cpn = other_cpn[other_cpn_name]['vms']
                                               instances_other_cpn[instance_id] = instances_data[instance_id]
                                               other_cpn[other_cpn_name]['vms'] = instances_other_cpn
                                               other_cpn[other_cpn_name]['nomes'][instance_id] = data[actual_cpn]['nomes'][instance_id]
                                               migration_flag = True
                                               migrations[actual_cpn][instance_id] = [ other_cpn_name , cpn_data[actual_cpn]['nomes'].get(instance_id) ,instances_id_project[instance_id]]
                                               #update future owner of instance
                                               owner_cpn_instance[instance_id] = {actual_cpn : other_cpn_name}
                                           else:
                                               continue
                                        else:
                                            break 
                                    else:
                                        migration_flag = False
                                else:
                                    continue
                            #update owner
                            if migration_flag == False:
                                if instance_id in owner_cpn_instance:
                                    if( owner_cpn_instance[instance_id].has_key(actual_cpn) or actual_cpn in owner_cpn_instance[instance_id].values()):
                                        continue
                                else:
                                    migrations[actual_cpn][instance_id] = None
                                    shutdown[actual_cpn] = False
                        if not actual_cpn in shutdown:
                            shutdown[actual_cpn] = True
                    else:
                         compute_nodes_copy.remove(cpn_data)
                         shutdown[actual_cpn] = True
                         continue  
                else:
                    compute_nodes_copy.remove(cpn_data)
                    shutdown[actual_cpn] = False
        except Exception as excp2:
                return {"error in algorithm suggestion":excp2.message}

        for host_key in migrations.keys():
            if None in migrations[host_key].values():
                migrations[host_key] = {}
        output = {} #json output with all data
        output['Hosts'] = shutdown
        output['Migracoes'] = migrations
        #recomendation = self.remove_duplicated_migrations(output)
        return output

    #Not using anymore
    #def remove_duplicated_migrations(self, output):
    #    result = output
    #    for compute_node in result['Migracoes'].keys():
    #        for server  in result['Migracoes'][compute_node].keys():
    #            if not self.__nova.verify_host_has_server(compute_node,server):
    #                result['Migracoes'][compute_node].pop(server)
    #    return result

    def cpu_util_from(self, timestamp_begin=None, timestamp_end=None, resource_id=None):
        return json.dumps(self.__ceilometer.get_cpu_util(timestamp_begin, timestamp_end, resource_id))

    def cpu_util_flavors(self, timestamp_begin=None, timestamp_end=None):
        data = self.__ceilometer.get_cpu_util_flavors(timestamp_begin, timestamp_end)
        ret = analytics.recommendations.recomenda_flavor(data)
        return json.dumps(ret)

    def projects_with_instances_and_cpu_util(self):
        projects = self.__keystone.tenants

        ret = { 'name' : 'cloud', 'children' : [] }

        for p in projects:
            proj = { 'name' : p.name, 'children' : [] }

            instances = self.__nova.instances(p.name)

            for i in instances:                 
                proj['children'].append({ 'resource_id' : i.id, 'instance_name' : i.name })

            ret['children'].append(proj)

        return ret

    def alarms_history(self, timestamp_begin=None, timestamp_end=None):
        return self.__ceilometer.get_alarms_history(timestamp_begin, timestamp_end)

    def add_alarm(self, name, resource, threshold, operator, period, ev_period, send_mail, email_admin, instance=""):
        return self.__ceilometer.set_alarm(name, resource, threshold, operator, period, ev_period, send_mail, email_admin, instance)

    def alarm_email(self, data_requested):
        alarm_id = ast.literal_eval(data_requested)['alarm_id']
        userId = self.__ceilometer.get_alarm_userid(alarm_id)
        projectId = self.__ceilometer.get_alarm_projectid(alarm_id)
        userEmail = self.__keystone.get_user_email(userId, projectId)
        copy_admin = self.__ceilometer.get_alarm_email_status(alarm_id)
        adminEmail = self.__keystone.get_user_email(self.__keystone.get_user(projectId,'admin'),projectId)



        if 'True' in copy_admin[0] and 'True' in copy_admin[1] :
            send_email('cloudtelemetry.service1@gmail.com',
                   [adminEmail],
                   [],
                   'Alert Telemetry Cloud',
                   'Email disparado pelo alarme!!!',
                   'cloudtelemetry.service1@gmail.com',
                   '4n4lyt1cs')

            send_email('cloudtelemetry.service1@gmail.com',
                   [userEmail],
                   [],
                   'Alert Telemetry Cloud',
                   'Email disparado pelo alarme!!!',
                   'cloudtelemetry.service1@gmail.com',
                   '4n4lyt1cs')

        elif 'True' in copy_admin[0] and 'False' in copy_admin[1]:
            send_email('cloudtelemetry.service1@gmail.com',
                   [userEmail],
                   [],
                   'Alert Telemetry Cloud',
                   'Email disparado pelo alarme!!!',
                   'cloudtelemetry.service1@gmail.com',
                   '4n4lyt1cs')

        elif 'False' in copy_admin[0] and 'True' in copy_admin[1]:
            send_email('cloudtelemetry.service1@gmail.com',
                   [adminEmail],
                   [],
                   'Alert Telemetry Cloud',
                   'Email disparado pelo alarme!!!',
                   'cloudtelemetry.service1@gmail.com',
                   '4n4lyt1cs')

    def alarm_description(self):
        return self.__ceilometer.get_alarm_parameters()
    
    def delete_alarm(self, alarm_id):
        return json.dumps(self.__ceilometer.delete_alarms(alarm_id))

    def hosts_cpu(self, timestamp_begin, timestamp_end):
        return self.__hosts_db.get_data_db('Cpu_Util', timestamp_begin, timestamp_end)

    def hosts_memory(self, timestamp_begin, timestamp_end):
        return self.__hosts_db.get_data_db('Memory', timestamp_begin, timestamp_end)

    def hosts_disk(self, timestamp_begin, timestamp_end):
        return self.__hosts_db.get_data_db('Disk', timestamp_begin, timestamp_end)

    def hosts_network(self, timestamp_begin, timestamp_end):
        return self.__hosts_db.get_data_db('Network', timestamp_begin, timestamp_end)

    def host_metrics(self, project):
        return self.__nova.metrics(project)

    def host_aggregates(self, project):
        return self.__nova.host_aggregates(project)

    def resource_host(self, host):
        return self.__nova.resource_host(host)


    def hosts_recommendation(self, r_cpu, r_memory , r_disk):
        resource = []
        ret = {}
        r_cpu = json.loads(r_cpu)
        r_memory = json.loads(r_memory)
        r_disk = json.loads(r_disk)
        for host in r_cpu:
            host_http = host["host_address"]
            if host["data"] is None:
                continue
            for data in host["data"]:
                resource.append(data["data"])
            resource = sorted(resource)
            if(len(resource)%2 == 0):
                index = len(resource)/2
                mediana = (resource[index-1] + resource[index+1])/2
            else:
                mediana = resource[int(math.ceil(len(resource)/2))]

            if mediana >= 95:
                ret[host_http] ="sobrecarregado"
            else:
                resource = []
                for host_mem in r_memory:
                    if(host["host_address"]  == host_mem["host_address"]):
                        for data in host_mem["data"]:
                            for value in json.loads(data["data"]):
                                resource.append(value["percent"])
                        resource = sorted(resource)

                if(len(resource)%2 == 0):
                    index = len(resource)/2
                    mediana = (resource[index-1] + resource[index+1])/2
                else:
                    mediana = resource[int(math.ceil(len(resource)/2))]

                if mediana >= 95:
                    ret[host_http] ="sobrecarregado"
                else:
                    ret[host_http] ="normal"       
        return json.dumps(ret)
        #return json.dumps(cpu)

    def instances_from_host(self, host_name):
        attr_host = 'OS-EXT-SRV-ATTR:host'
        ret = []
        projects = self.__keystone.projects
        for project in projects:
            instances = self.__nova.instances(project['name'])
            for instance in instances:
                print instance._info
                if instance._info[attr_host] == host_name:
                    ret.append({'instance_name' : instance.name, 'instance_id' : instance.id})
        return ret   

    def migrate_to_host(self, project_name, host_name, instance_id):
        #host_vm = self.__nova.vm_hostname(project_name,instance_id)
        #attr_host = 'OS-EXT-SRV-ATTR:host'
        #if host_vm._info[attr_host] == host_name:
        #    raise MigrateException(400,"Migracao para o mesmo destino")
	#elif host_vm._info[attr_host] == 'truta' and host_name != 'truta':
        #    raise MigrateException(500,"Migracao de host para compute node")
        #else:
        try:
            retorno = self.__nova.vm_migration(project_name,host_name,instance_id)
        except Exception as a:
            return {"erro":a.message}
        return {"status":"success"}


    def get_benchmark_bd(self):
        ret = self.__benchmark_db.get_data_db()
        return ret


    def start_instance_bench(self, project, host):
        return self.__nova.start_instance_bench(project, host)


    def get_benchmark(self, project, host):
        benchmark_ip = self.__nova.get_benchmark_ip(project, host)
        data = requests.get('http://'+benchmark_ip+':5151/get_benchmarking')
        return data.json()
 
    def get_benchmark_status(self, project, host):
        benchmark_ip = self.__nova.get_benchmark_ip(project, host)
        print benchmark_ip
        data = requests.get('http://'+benchmark_ip+':5151/get_status')
        return data.text

    def repeat_benchmark(self, project):
        benchmark_ip = self.__nova.get_benchmark_ip(project)
        data = requests.get('http://'+benchmark_ip+':5151/start_benchmarking')
        return data.text

    def remove_benchmark_instance(self, host):
        id = self.__nova.benchmark_id(host)
        if id == None:
            return "sem instancia benchmark"
        else:
            remove = self.__nova.remove_instance(id)
            return remove

    def hosts_aggregation_cpu(self, timestamp_begin=None, timestamp_end=None):
        ret = []

        cpu_data = self.hosts_cpu(timestamp_begin, timestamp_end)
        aggregates = self.__nova.host_aggregates('admin')

        for aggregate in aggregates:
            result = []
            host_address = aggregate["host_address"]
            for host in host_address:
                host_name = self.__nova.server_name_by_ip(host)
                host_cpu = self.__nova.resource_host(host_name)["cpu"]
                
                for data in cpu_data:
                    if(data["host_address"]==host):
                        convert = []

                        for cpu_percent in data["data"]:
                            cpu_percent["data"] = (1 - cpu_percent["data"]/100.0)* host_cpu
                            convert.append(cpu_percent)
 
                        if(len(result)==0):
                            result = convert
                        else:
                            if(len(result) > len(convert)):
                                result = result[0:len(convert)]
                            for i in range(len(result)):
                                value = result[i]
                                value["data"] = value["data"] + (convert[i])["data"]
                                result[i] = value
                                
                        break
            ret.append({"Aggregate":aggregate["name"], "data":result})
        return json.dumps(ret)

    def hosts_aggregation_memory(self, timestamp_begin=None, timestamp_end=None):
        ret = []

        memory_data = self.hosts_memory(timestamp_begin, timestamp_end)
        aggregates = self.__nova.host_aggregates('admin')

        for aggregate in aggregates:
            result = []
            host_address = aggregate["host_address"]
            aggregate_memory = self.__nova.resource_aggregates(aggregate['name'])['memory_mb']
            for host in host_address:	
                host_name = self.__nova.server_name_by_ip(host)
                host_memory = self.__nova.resource_host(host_name)["memory_mb"]

                for data in memory_data:
                    if(data["host_address"]==host):
                        convert = []

                        for memory_percent in data["data"]:
                            memory_percent['data'] = ((json.loads(memory_percent['data'])[0]['percent']/100.0 )*host_memory)/aggregate_memory
                            convert.append(memory_percent)

                        if(len(result)==0):
                            result = convert
                        else:
                            if(len(result) > len(convert)):
                                result = result[0:len(convert)]
                            for i in range(len(result)):
                                value = result[i]
                                value["data"] = (value["data"] + (convert[i])["data"])
                                result[i] = value

                        break
            ret.append({"Aggregate":aggregate["name"], "data":result})
        return json.dumps(ret)


    def hosts_aggregation_disk(self, timestamp_begin=None, timestamp_end=None):
        ret = []

        disk_data = self.hosts_disk(timestamp_begin, timestamp_end)
        aggregates = self.__nova.host_aggregates('admin')

        for aggregate in aggregates:
            result = []
            host_address = aggregate["host_address"]
            aggregate_disk = self.__nova.resource_aggregates(aggregate['name'])['disk']
            for host in host_address:
                host_name = self.__nova.server_name_by_ip(host)
                host_disk = self.__nova.resource_host(host_name)["disk_gb"]

                for data in disk_data:
                    if(data["host_address"]==host):
                        convert = []

                        for disk_percent in data["data"]:
                            disk_percent['data'] = ((json.loads(disk_percent['data'])[0]['percent']/100)*host_disk)/aggregate_disk
                            convert.append(disk_percent)

                        if(len(result)==0):
                            result = convert
                        else:
                            if(len(result) > len(convert)):
                                result = result[0:len(convert)]
                            for i in range(len(result)):
                                value = result[i]
                                value["data"] = value["data"] + (convert[i])["data"]
                                result[i] = value

                        break
            ret.append({"Aggregate":aggregate["name"], "data":result})
        
        return json.dumps(ret)

    def hosts_aggregation_network(self, timestamp_begin=None, timestamp_end=None):
        ret = []

        network_data = self.hosts_network(timestamp_begin, timestamp_end)
        aggregates = self.__nova.host_aggregates('admin')

        for aggregate in aggregates:
            result = []
            host_address = aggregate["host_address"]
            for host in host_address:
                for data in network_data:
                    if(data["host_address"]==host):
                        convert = []

                        for network_io in data["data"]:
                            network_io_all=json.loads(network_io['data'])[0]
                            network_io['data'] = {'net_bytes_sent': network_io_all['net_bytes_sent'], 'net_bytes_recv': network_io_all['net_bytes_recv']}

                            convert.append(network_io)

                        if(len(result)==0):
                            result = convert
                        else:
                            if(len(result) > len(convert)):
                                result = result[0:len(convert)]
                            for i in range(len(result)):
                                value = result[i]
                                #value["data"] = value["data"] + (convert[i])["data"]
                                result[i] = value

                        break
            ret.append({"Aggregate":aggregate["name"], "data":result})

        return json.dumps(ret)

        #implementar como e o aggregate e dados a apresentar
        #return json.dumps([{"Aggregate":"AggTeste", "data":[{'timestamp': '2014-10-13T17:52:14', 'data': 0.0565}]}])

    def points_reduction_by_server_cpu(self, timestamp_begin, timestamp_end, hosts):
        data = []
        old_data = self.hosts_cpu(timestamp_begin, timestamp_end)
        key = 'data'
        if len(old_data)==0 or len(old_data[0][key]) <= 3:
           result = old_data
        else:
            for host in range(len(hosts)):
                dict_host = {}
                dict_host["host_address"] = hosts[host]
                dict_host['data'] = self.__reduction.points_reduction(old_data[host]['data'],key)
                data.append(dict_host)
                result = data
        return result
    
    def points_reduction_by_server_memory(self, timestamp_begin, timestamp_end, hosts):
        data = []
        old_data = self.hosts_memory(timestamp_begin, timestamp_end)
        key = 'data'
        if len(old_data)==0 or len(old_data[0][key]) <= 3:
           result = old_data
        else:
            for host in range(len(hosts)):
                dict_host = {}
                dict_host["host_address"] = hosts[host]
                dict_host['data'] = self.__reduction.points_reduction_for_percent(old_data[host]['data'],key)
                data.append(dict_host)
                result = data
        return result

    def points_reduction_by_server_disk(self, timestamp_begin, timestamp_end, hosts):
        data = []
        old_data = self.hosts_disk(timestamp_begin, timestamp_end)
        if len(old_data)==0 or len(old_data[0]['data']) <= 3:
           result = old_data
        else:
            for host in range(len(hosts)):
                dict_host = {}
                dict_host["host_address"] = hosts[host]
                dict_host['data'] = self.__reduction.points_reduction_disk(old_data[host]['data'])
                data.append(dict_host)
                result = data

        return result

    def points_reduction_by_server_network(self, timestamp_begin, timestamp_end, hosts):
        #implementar a funcao de reducao dos pontos
        return []

    def points_reduction_vm(self, timestamp_begin,timestamp_end,resource_id):
        old_data = json.loads(self.cpu_util_from(timestamp_begin,timestamp_end,resource_id))
        key2 = "cpu_util_percent"
        data = self.__reduction.points_reduction(old_data,key2)
        return data

    def vm_info(self):
        ret = []
        project = []

        for project_data in json.loads(self.projects()):
            project.append(project_data["name"])
        
        for project_name in project:
            informations =  self.__nova.vm_info(project)
            vms_data = {}
            for node in informations:
                for node_name in node.keys():
                    vms_name = (node[node_name])['nomes']
                    for key in vms_name.keys():
                        vms_data[key] = vms_name[key]

            ret.append({project_name:vms_data})

        return ret

    def instances_by_project(self):
        project = []

        for project_data in json.loads(self.projects()):
            project.append(project_data["name"])

        informations =  self.__nova.vm_info(project)
       
        vms_data = {}

        for node in informations:
            for node_name in node.keys():
                project_name = (node[node_name])['Info_project']
                vms_name = (node[node_name])['nomes']
                for key in project_name.keys():
                    for instance_id in project_name[key]:
                        if not (key in vms_data.keys()):
                            vms_data[key] = {}
                            vms_data[key][instance_id] = vms_name[instance_id]
                        else:
                            vms_data[key][instance_id] = vms_name[instance_id]

        return vms_data
 
    def vcpus_for_aggregate(self, project):
        return json.dumps(self.__nova.vcpus_for_aggregate(project))
