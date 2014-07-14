import subprocess
import json, requests
import env
from keystone_client import KeystoneClient
from novaclient.v3 import client
from novaclient.v3.servers import ServerManager

class NovaClient:

    def instances(self, project):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project, env.OS_AUTH_URL)
        return nova.servers.list()

    def metrics(self, project):

        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project, env.OS_AUTH_URL)
        hosts = nova.hosts.list()
        nome_dos_hosts = []
        dic_dos_hosts = {}
        for host in hosts:
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

        return json.dumps(dic_dos_hosts)


    def host_describe(self, host_name):
        auth_tokens_url = env.OS_AUTH_URL + '/tokens'
        headers = {'Content-Type':'application/json','Accept':'application/json'}
        payload = {"auth": {"tenantName": env.OS_ADMIN_TENANT, "passwordCredentials": {"username": env.OS_USERNAME, "password": env.OS_PASSWORD}}}

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
        os_hosts_url = admin_url + '/os-hosts/' + host_name

        r = requests.get(os_hosts_url, headers=headers)
        if r.status_code != 200:
            msg = 'Host info request error. HTTP error ' + str(r.status_code)
            raise Exception(msg)

        return r.json()
        
    def vm_migration(self,project_name,host_name,instance_id):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project_name, env.OS_AUTH_URL)
        server = ServerManager(nova)
        block = True
        disk_commit = False 
        server.live_migrate(instance_id,host_name,block,disk_commit)

    def vm_hostname(self,project_name,instance_id):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project_name, env.OS_AUTH_URL)
        server = ServerManager(nova)
        return server.get(instance_id)

    def flavor_information(self, project):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project, env.OS_AUTH_URL)
        dic_flavors = {}
        lista_flavors = nova.flavors.list()
        for flavor in lista_flavors:
            lista_valores = [flavor.vcpus,flavor.ram,flavor.disk]
            dic_flavors[flavor.id] = lista_valores
        return dic_flavors

    def vm_info(self,projects):
        dic_hosts = {}
        host_statistics = json.loads( self.metrics(projects[0]) )
        keys = host_statistics.keys()
        for host in keys:
            dic_hosts[host] = {'Total':host_statistics[host]['Total'], 'Livre': [a - b for a,b in zip(host_statistics[host]['Total'],host_statistics[host]['Em uso']) ] , 'vms':{} , 'nomes':{} }
        for p in projects:
            nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, p, env.OS_AUTH_URL)
            flavors = self.flavor_information(p)
            vm_list = nova.servers.list()
            if len(vm_list) > 0:
                for vm in vm_list:
                    if vm._info['os-extended-server-attributes:host'] == None:
                        pass
                    else:
                        dic_hosts[vm._info['os-extended-server-attributes:host']]['vms'][vm.id] = flavors[vm.flavor['id']]
                        dic_hosts[vm._info['os-extended-server-attributes:host']]['nomes'][vm.id] = vm._info['name']
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

    def start_instance_bench(self, project):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project, env.OS_AUTH_URL)
        servers = nova.servers.list()
        for server in servers:
            if server.name == 'benchmark':
                return 'ja ha uma instancia chamada benchmark'
        nova.servers.create('benchmark', '330a1d0b-5dc4-4dac-b83f-a45212abf5fd', '4d8a8f1a-2a43-4b0c-9af6-7e379a2358b8', availability_zone='nova:truta')
        return 'instancia disparada'

    def get_benchmark_ip(self, project):
        nova = client.Client(env.OS_USERNAME, env.OS_PASSWORD, project, env.OS_AUTH_URL)
        servers = nova.servers.list()
        benchmark_id  = ' '
        for server in servers:
            if server.name == 'benchmark':
                benchmark_id = server.id
        if benchmark_id == ' ':
            return 'nao ha instancia de benchmark'
        instance_bench = nova.servers.get(benchmark_id)
        return instance_bench.addresses['private'][0]['addr']

    def remove_instance(self, id):
        nova = client.Client(env.OS_USERNAME,env.OS_PASSWORD,"admin",env.OS_AUTH_URL)
        sm = ServerManager(nova)
        instancia = sm.get(id)
        sm.delete(instancia)
        return True

    def benchmark_id(self):
        nova = client.Client(env.OS_USERNAME,env.OS_PASSWORD,"admin",env.OS_AUTH_URL)
        servers = nova.servers.list()
        for server in servers:
            if server.name != 'benchmark':
                 pass
            else:
                 return server.id
        return None
              
    def server_get_ip_by_name(self, host_name):
        hosts = {'truta':'150.165.15.4', 'cloud-analytics1':'150.165.15.38'  ,'cloud-analytics2':'150.165.15.42'}
        return hosts[host_name]

    def host_aggregates(self, project):
        nova = client.Client(env.OS_USERNAME,env.OS_PASSWORD,project,env.OS_AUTH_URL)
        aggregates = nova.aggregates.list()
        aggregates_hosts = []        
        for aggregate in aggregates:
            hosts_list = []
            for host in aggregate.hosts:
                hosts_list.append(self.server_get_ip_by_name(host))
            aggregates_hosts.append({'name':aggregate.name, 'host_address':hosts_list})
        return aggregates_hosts

    def server_name_by_ip(self, ip):
        hosts = {'150.165.15.4':'truta', '150.165.15.38':'cloud-analytics1'  ,'150.165.15.42':'cloud-analytics1'}
        return hosts[ip]


    def resource_host(self, host):
        return self.host_describe(host)['host'][0]['resource']



    def resource_aggregates(self, name):

        nova = client.Client(env.OS_USERNAME,env.OS_PASSWORD,'admin',env.OS_AUTH_URL)
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
        nova = client.Client(env.OS_USERNAME,env.OS_PASSWORD,project,env.OS_AUTH_URL)
        instances = nova.servers.list()
        has_meta = []
        for instance in instances:
            meta = instance.metadata
            if meta.has_key('critical'):
                if meta['critical'] == 'true':
                    has_meta.append(instance.id)
        return has_meta
