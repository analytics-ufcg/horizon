import ast
from keystoneclient.v2_0 import client

class KeystoneClient:

    def __init__(self, config):
        self.__os_username = config.get('Openstack', 'osusername')
        self.__os_password = config.get('Openstack', 'ospassword')
        self.__os_auth_url = config.get('Openstack', 'osauthurl')
        self.__admin_tenant_id = config.get('Openstack', 'AdminTenantId')
        self.__keystone = client.Client(username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        self.projects = [ {'name' : i.name, 'id' : i.id} for i in self.__keystone.tenants.list() ] 
        self.tenants = self.__keystone.tenants.list()

    def get_user_email(self, user_id):
        project_id = self.__admin_tenant_id
        keystone = client.Client(tenant_id=project_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        userData = str(keystone.users.get(user_id))[6:-1]
        return ast.literal_eval(userData)['email']

    def list_users(self):
        keystone = client.Client(tenant_id=self.__admin_tenant_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        users = []
        for user in keystone.users.list():
            users.append(user)
        return users

    def get_user(self, name):
        project_id=self.__admin_tenant_id        
        keystone = client.Client(tenant_id=project_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        for user in keystone.users.list():
            if user.username == name:
                return user
        return None

    def get_username(self, user_id):
        project_id = self.__admin_tenant_id
        keystone = client.Client(tenant_id=project_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        for user in keystone.users.list():
            if user.id == user_id:
                return user
        return None


    def list_project_users(self, tenant_id):
        project_id = self.__admin_tenant_id
        keystone = client.Client(tenant_id=project_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        users = keystone.tenants.list_users(tenant_id)
        users_list = []
        for user in users:
            if user.id not in users_list:
                users_list.append(user.id)

        return users_list


    def get_tenants(self):
        project_id = self.__admin_tenant_id
        keystone = client.Client(tenant_id=project_id, username=self.__os_username, password=self.__os_password, auth_url=self.__os_auth_url)
        return keystone.tenants.list()
