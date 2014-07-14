import MySQLdb as mdb

def get_latest_cpu_util_from_database(resource_id=None, project_id=None, limit=None):
    try:
        con = mdb.connect('localhost', 'root', 'pass', 'ceilometer');

        query = 'SELECT * FROM meter WHERE counter_name=\"cpu_util\"'

        if resource_id:
            query = query + ' AND resource_id=\"%s\"' % resource_id

        if project_id:
            query = query + ' AND project_id=\"%s\"' % project_id

        query = query + ' ORDER BY timestamp DESC'
        
        if limit >= 0:
            query = query + ' LIMIT %d' % limit

        cur = con.cursor()

        cur.execute(query)

        rows = cur.fetchall()
    
        return rows    
    except mdb.Error, e:  
        print "Error %d: %s" % (e.args[0],e.args[1])
        return None
    finally:    
        if con:    
            con.close()

