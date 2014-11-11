import MySQLdb as mdb
import json

class HostDataDBWriter:

    def __init__(self, server='localhost', user='root', password='pass', db='hosts_data', table='hosts_data_table'):
        try:
            self.con = mdb.connect(server, user, password, db)
            self.table = table;
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            return None

    def save_data_db(self, cpu=0.0, memory=None, disk=None, network=None, service_status=None, host_status='T', host=None):
        cursor = self.con.cursor()
        try:
            query = "INSERT INTO %s (Date, Cpu_Util, Memory, Disk, Network, ServiceStatus, HostStatus, Host) VALUES(CURRENT_TIMESTAMP(), %f, '%s', '%s', '%s', '%s', '%s', '%s')" % (self.table, cpu, json.dumps(memory), json.dumps(disk), json.dumps(network), json.dumps(service_status), host_status, host)
            #print query
            cursor.execute(query)
            self.con.commit()
            return "sucess"
        except Exception, e:
            print e
            return None
        finally:
            cursor.close()