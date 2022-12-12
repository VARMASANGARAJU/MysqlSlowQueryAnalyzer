from collections import defaultdict
import sys
import random
import subprocess

from django.http import HttpResponse

from mysql_app.models import QueryData


def savelogs(logList,intance_obj):
    if intance_obj.status == True:
        query_data = QueryData.objects.filter(instance_id=intance_obj.id)
        query_data.delete()
    for logDict in logList:
        newQueryData = QueryData()
        newQueryData.instance = intance_obj
        newQueryData.count = logDict.get('Count',0)
        newQueryData.time =  logDict.get('Time',0)
        newQueryData.lock = logDict.get('Lock',0)
        newQueryData.rows = logDict.get('Rows',0)
        newQueryData.slow_query = logDict.get('Query',"Empty")
        newQueryData.save()
    return True

def fetchLogs(intance_obj):
    instance_user = intance_obj.user
    instance_ip = intance_obj.ip_address
    instance_slow_query_path =  "/var/log/mysql/mysql-slow.log" if not intance_obj.log_file_path else intance_obj.log_file_path 
    
    temp_file = "slowquery__"+str(random.randint(100,100000))+".log"
    subprocess.Popen(f"ssh {instance_user}@{instance_ip} mysqldumpslow -a -s t {instance_slow_query_path} >> {temp_file}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    SKIP = 2

    all_data = []
    with open(temp_file) as log:
        for _ in range(SKIP):
            next(log)
        i = 0
        for line in log:
            try:
                if "Time=" and "Lock=" in line:
                    single_data = {}
                    query_meta_data = line.split("  ")
                    # ['Count: 17', 'Time=2.02s (34s)', 'Lock=0.00s (0s)', 'Rows=21.0 (357), root[root]@localhost\n']
                    for data in query_meta_data:
                        if ":" in data:
                            single_data['Count'] = data.split(':')[1].strip()
                        elif "=" in data:
                            meta_data = data.split('=')
                            single_data[meta_data[0]] = meta_data[1].split(' ')[0].replace('s','')
                            single_data[meta_data[0]+'Extra'] = meta_data[1].split(' ')[1].replace('(','').replace('s','').replace(')','')

                elif "SELECT" in line:
                    single_data['Query'] = line.strip()
                    all_data.append(single_data)
            except ValueError:
                        pass
    creation_check = savelogs(all_data, intance_obj)
    return creation_check