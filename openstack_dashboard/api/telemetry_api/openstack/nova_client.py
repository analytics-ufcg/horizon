import subprocess
import json, requests, ast, datetime
from keystone_client import KeystoneClient
from novaclient.v3 import client
from novaclient.v3.servers import ServerManager
import novaclient

class NovaClient:

    def __init__(self, config):
        self.__os_username = config.get('Openstack', 'osusername')
        self.__os_password = config.get('Openstack', 'ospassword')
        self.__os_auth_url = config.get('Openstack', 'osauthurl')
        self.__os_tenant_admin = config.get('Openstack', 'ostenantadmin')
        self.__os_compute_nodes = ast.literal_eval(config.get('Openstack', 'computenodesmap'))

    def instances(self, project):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project, self.__os_auth_url)
        return nova.servers.list()

    def metrics(self, project):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project, self.__os_auth_url)
        hosts = nova.hosts.list()
        nome_dos_hosts = []
        dic_dos_hosts = {}
        for host in hosts:
            if host.service == 'compute':
                corte = str(host)[7:-1]
                nome_dos_hosts.append(corte)
        nome_dos_hosts = list(set(nome_dos_hosts))

        for host in nome_dos_hosts:
            descricao = self.host_describe(host)

            cpu_total = descricao['host'][0]['resource']['cpu']
            memoria_total =  descricao['host'][0]['resource']['memory_mb']
            disco_total =  descricao['host'][0]['resource']['disk_gb']

            cpu_usado = descricao['host'][1]['resource']['cpu']
            memoria_usado =  descricao['host'][1]['resource']['memory_mb']
            disco_usado =  descricao['host'][1]['resource']['disk_gb']

            dic =  {'Total':[], 'Em uso':[], 'Percentual': []}

            dic['Total'] = [cpu_total, memoria_total, disco_total]
            dic['Em uso'] = [cpu_usado, memoria_usado, disco_usado]
            dic['Percentual'] = [round(float(cpu_usado)/cpu_total,3), round(float(memoria_usado)/memoria_total, 3), round(float(disco_usado)/disco_total,3)]

            dic_dos_hosts[host] = dic

        return dic_dos_hosts

    def verify_host_has_server(self, host_name, server_id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, 'admin', self.__os_auth_url)
        server = nova.servers.get(server_id)
        if server._info['OS-EXT-SRV-ATTR:host'] == host_name:
            return True
        return False

    def list_compute_nodes(self):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, 'admin', self.__os_auth_url)
        hosts = nova.hosts.list()
        compute_nodes = []
        for host in hosts:
            if host._info['service']=='compute':
                compute_nodes.append(host)
        return compute_nodes

    def get_servers_by_host(self, host_name):
        servers = self.list_all_instances()
        host_servers = []
        for server in servers:
            if server['OS-EXT-SRV-ATTR:host'] == host_name:
                host_servers.append(server)
        return host_servers

    def get_servers_by_project(self, project_id):
        servers = self.list_all_instances()
        project_servers = []
        for server in servers:
            if server['tenant_id'] == project_id:
                project_servers.append(server)
        return project_servers


    def get_users_by_host(self, host_servers):
        users_id = []
        instances = []
        for server in host_servers:
            if server['id'] not in instances:
                instances.append(server['id'])
                users_id.append(server['user_id'])
        return users_id

    def get_instance_users_by_host(self, host_servers):
        users_id = {}
        instances = []
        for server in host_servers:
            if server['id'] not in instances:
                instances.append(server['id'])
                users_id[server['id']] = server['user_id']
        return users_id

    def get_instance_users_by_project(self, host_projects):
        users_id = {}
        instances = []
        for server in host_projects:
            if server['id'] not in instances:
                instances.append(server['id'])
                users_id[server['id']] = server['user_id']
        return users_id

    def get_user_instances(self, user_id):
        servers = self.list_all_instances()
        instances = {}
        for server in servers:
            if server['user_id'] == user_id:
                instances[server['id']] = server['name']
        return instances

    def get_nova_urls(self, url):
        auth_tokens_url = self.__os_auth_url + '/tokens'
        headers = {'Content-Type':'application/json','Accept':'application/json'}
        payload = {"auth": {"tenantName": self.__os_tenant_admin, "passwordCredentials": {"username": self.__os_username, "password": self.__os_password}}}


        r = requests.post(auth_tokens_url, data=json.dumps(payload), headers=headers)
        if r.status_code != 200:
            msg = 'Token request error. HTTP error ' + str(r.status_code)
            raise Exception(msg)

        response = r.json()

        token = response['access']['token']['id']
        compute_service = None
        for s in response['access']['serviceCatalog']:
            if s['type'] == 'compute':
                compute_service = s
                break

        if compute_service is None:
            raise Exception('could not retrieve compute service (nova)')

        admin_url = compute_service['endpoints'][0]['adminURL']
        headers = {'X-Auth-Project-Id':'admin', 'Accept':'application/json', 'X-Auth-Token':token}
    


        os_hosts_url = admin_url + url
        r = requests.get(os_hosts_url, headers=headers)
        if r.status_code != 200:
            msg = 'Host info request error. HTTP error ' + str(r.status_code)
            raise Exception(msg)

        return r.json()

    def host_describe(self, host_name):
        url = '/os-hosts/' + host_name
        return self.get_nova_urls(url)

    def images_list(self):
        url = '/images/detail'
        return self.get_nova_urls(url)

    def list_all_instances(self):
        url = '/servers/detail?all_tenants=True'
        return self.get_nova_urls(url)['servers']
        
    def vm_migration(self,project_name,host_name,instance_id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project_name, self.__os_auth_url)
        try:
            nova.servers.live_migrate(instance_id, host_name, True, False)
        except Exception as e:
            raise Exception(e.message)
        return "Ok"
  
    def vm_hostname(self,project_name,instance_id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project_name, self.__os_auth_url)
        return nova.servers.get(instance_id)

    def flavor_information(self, project):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project, self.__os_auth_url)
        dic_flavors = {}
        lista_flavors = nova.flavors.list()
        for flavor in lista_flavors:
            lista_valores = [flavor.vcpus,flavor.ram,flavor.disk]
            dic_flavors[flavor.id] = lista_valores
        return dic_flavors

    def vm_info(self,projects):
        dic_hosts = {}
        attr_host = 'OS-EXT-SRV-ATTR:host'
        host_statistics = self.metrics(projects[0])
        keys = host_statistics.keys()
        for host in keys:
            dic_hosts[host] = {'Total':host_statistics[host]['Total'],'Info_project':{}, 'Livre': [a - b for a,b in zip(host_statistics[host]['Total'],host_statistics[host]['Em uso']) ] , 'vms':{} , 'nomes':{} }
        for p in projects:
            from novaclient.v1_1 import client # nova client v3 raises exception for this
            nova = client.Client(self.__os_username, self.__os_password, p, self.__os_auth_url)
            flavors = self.flavor_information(p)
            vm_list = nova.servers.list()
            list_instances =[]
            for vm in vm_list:
                dic_hosts[vm._info[attr_host]]['vms'][vm.id] = flavors[vm.flavor['id']]
                dic_hosts[vm._info[attr_host]]['nomes'][vm.id] = vm._info['name']
                list_instances.append(vm.id)
                if(str(p) not in dic_hosts[vm._info[attr_host]]['Info_project'].keys()):
                    dic_hosts[vm._info[attr_host]]['Info_project'][str(p)] = [vm.id]
                else:
                    dic_hosts[vm._info[attr_host]]['Info_project'][str(p)].append(vm.id)
        lista_ordenada = []
        dic_ord = sorted( dic_hosts.items(), key=lambda x: (  len( x[1]['vms'].keys() )==0, -x[1]['Livre'][0] ))
        for e in dic_ord:
            dic_aux = {}
            dic_aux[e[0]] = e[1]
            lista_ordenada.append(dic_aux)
        lista_ordenada2 = lista_ordenada[:]
        for dic in lista_ordenada:
            if len( dic[dic.keys()[0]]['vms'].keys()) == 0:
               lista_ordenada2.remove(dic)
               lista_ordenada2.insert(0,dic)
        return lista_ordenada2 
  

    def get_benchmark_id(self):
        from novaclient.v1_1 import client
        nova = client.Client(self.__os_username, self.__os_password, 'admin', self.__os_auth_url)
        images = self.images_list()['images']
        for image in images:
            if image['name']==  'ubuntu-benchmark':
                return image['id']
        return False        
        

    def get_benchmark_flavor(self):
        from novaclient.v1_1 import client
        nova = client.Client(self.__os_username, self.__os_password, 'admin', self.__os_auth_url)
        flavors_begin = nova.flavors.list()
        has_flavor = False
        for flavor in flavors_begin:
            if flavor.name == 'benchmark-flavor':
                return flavor.id
        bench_flavor = nova.flavors.create('benchmark-flavor', 1024, 1, 6)
        return bench_flavor.id

    def start_instance_bench(self, project, host_name):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project, self.__os_auth_url)
        servers = nova.servers.list()
        for server in servers:
            if server.name == 'benchmark-'+host_name:
                return False
        hosts_name = self.__os_compute_nodes.keys()
        nova.servers.create('benchmark-'+host_name, self.get_benchmark_id(), self.get_benchmark_flavor(), availability_zone='nova:'+host_name, nics=[{'net-id':'68f33fc4-9a9e-48bd-9e00-9f3b23dab808'}])
        return True

    def get_benchmark_ip(self, project, host_name):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username, self.__os_password, project, self.__os_auth_url)
        servers = nova.servers.list()
        benchmark_id  = ' '
        for server in servers:
            if server.name == 'benchmark-'+host_name:
                benchmark_id = server.id
        if benchmark_id == ' ':
            return 'nao ha instancia de benchmark'
        instance_bench = nova.servers.get(benchmark_id)
        return instance_bench.addresses['admin-net'][0]['addr']

    def remove_instance(self, id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,"admin",self.__os_auth_url)
        sm = ServerManager(nova)
        instancia = sm.get(id)
        sm.delete(instancia)
        return True

    def benchmark_id(self, host):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,'admin',self.__os_auth_url)
        servers = nova.servers.list()
        for server in servers:
            if server.name != 'benchmark-'+host:
                 pass
            else:
                 return server.id
        return None
              
    def server_get_ip_by_name(self, host_name):
        return self.__os_compute_nodes[host_name]

    def host_aggregates(self, project):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,project,self.__os_auth_url)
        aggregates = nova.aggregates.list()
        aggregates_hosts = []        
        for aggregate in aggregates:
            hosts_list = []
            for host in aggregate.hosts:
                hosts_list.append(self.server_get_ip_by_name(host))
            aggregates_hosts.append({'name':aggregate.name, 'host_address':hosts_list})
        return aggregates_hosts

    def server_name_by_ip(self, ip):
        for name, serv_ip in self.__os_compute_nodes.iteritems():
            if serv_ip == ip:
                return name
        return None

    def resource_host(self, host):
        return self.host_describe(host)['host'][0]['resource']

    def resource_aggregates(self, name):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,self.__os_tenant_admin,self.__os_auth_url)
        aggregates = nova.aggregates.list()

        for aggregate in aggregates:
            if aggregate.name == name:
                hosts = aggregate.hosts
                cpu = 0
                memory = 0
                disk = 0
                for host in hosts:
                    resource = self.resource_host(host)
                    cpu +=resource['cpu']
                    memory += resource['memory_mb']
                    disk += resource['disk_gb']
                return {'cpu':cpu,'memory_mb':memory,'disk':disk}
            else:
                pass

        return None

    def critical_instances(self, project):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        has_meta = []
        for i in project:
            nova = client.Client(self.__os_username,self.__os_password,i,self.__os_auth_url)
            instances = nova.servers.list()
            for instance in instances:
                meta = instance.metadata
                if meta.has_key('critical'):
                    if meta['critical'] == 'true':
                        has_meta.append(instance.id)
        return has_meta

    def vcpus_for_aggregate(self, project):
        aggregates = self.host_aggregates(project)
        ret = []
        for hosts in aggregates:
            total_vcpus = 0
            total_cpus = 0
            for host in hosts['host_address']:
                host_name = self.server_name_by_ip(host)
                host_data = self.host_describe(host_name)
                for instance in host_data['host']:
                    if((instance['resource'])['project']=='(used_now)'):
                        total_vcpus += (instance['resource'])['cpu']
                    if((instance['resource'])['project']=='(total)'):
                        total_cpus += (instance['resource'])['cpu']
            ret.append('{"name":' + '"' + hosts["name"] + '"' + ', "vcpus":' + str(total_vcpus) + ', "cpus":' + str(total_cpus)  + '}')
        return ret

    def create_snapshot(self, instance_id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,self.__os_tenant_admin, self.__os_auth_url)

        server_manager = ServerManager(nova)
        instance_obj = server_manager.get(instance_id)
        snapshot_name = 'snapshot--%s--%s' % (instance_obj.name, datetime.datetime.now())
        print snapshot_name
        nova.servers.create_image(instance_id, snapshot_name)

    def suspend_instance(self, instance_id):
        from novaclient.v1_1 import client # nova client v3 raises exception for this
        nova = client.Client(self.__os_username,self.__os_password,self.__os_tenant_admin, self.__os_auth_url)
        server_manager = ServerManager(nova)
        server_manager.suspend(instance_id)

