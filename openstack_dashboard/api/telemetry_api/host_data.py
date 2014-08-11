import MySQLdb as mdb
import time, datetime, json

class HostDataHandler:

    def __init__(self, server='localhost', user='root', password='pass', db='hosts_data', table='hosts_data_table'):
        try:
            self.con = mdb.connect(server, user, password, db)
            self.table = table;
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            return None

    def save_data_db(self, cpu, memory, disk, host):
        cursor = self.con.cursor()
        try:
            query = "INSERT INTO %s (Date, Cpu_Util, Memory, Disk, Host) VALUES(CURRENT_TIMESTAMP(), %f, '%s', '%s', '%s')" % (self.table, cpu, json.dumps(memory), json.dumps(disk), host)
            #print query
            cursor.execute(query)
            self.con.commit()
            return "sucess"    
        except Exception, e:  
            print e
            return None
        finally:
            cursor.close()

    def get_data_db(self, data, timestamp_begin=None, timestamp_end=None):
        cursor = self.con.cursor()
        try:
            query = "SELECT Date, %s, Host FROM %s" % (data, self.table)

            where = '' 
            if any([timestamp_begin, timestamp_end]):
                where += ' WHERE '
                if timestamp_begin:
                    where += "Date > \'%s\'" % datetime.datetime.strptime(timestamp_begin, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

                    if timestamp_end:
                        where += " AND Date < \'%s\'" % datetime.datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

            query += where
            print query
            
            cursor.execute(query)
            self.con.commit()
            
            rows = cursor.fetchall()

            ret = []
            for row in rows:
                found = False
                for data_host in ret:
                    if(row[2] == data_host['host_address']):
                        index = ret.index(data_host)
                        current = data_host['data']
                        current.append({'timestamp' : row[0].strftime('%Y-%m-%dT%H:%M:%S'), 'data' : row[1]})
                        data_host['data'] = current
                        ret[index] = data_host
                        found = True
                        break
                if(not found):
                    ret.append({'host_address':row[2], 'data':[{'timestamp' : row[0].strftime('%Y-%m-%dT%H:%M:%S'), 'data' : row[1]}]})
            
            return ret
        except Exception, e:
            print e
            return None
        finally:
           cursor.close() 

    def close_db(self):
        try:
            self.con.close()
        except:
            print 'Cant close connection'
