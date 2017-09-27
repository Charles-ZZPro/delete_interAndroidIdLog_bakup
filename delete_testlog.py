#-*-coding:utf-8-*-

###
# ver:     0.02
# date:    2017-08-24
# author:  Charles.Z
# change log:
#     unique item in StatUser bug fixed by specifying time
###

from __future__ import print_function
from __future__ import unicode_literals
from leancloud import Object
from leancloud import Query
from leancloud.errors import LeanCloudError
import leancloud
import time
import datetime
import hashlib
from random import Random
import sys
import datetime

# leancloud.init("Fhdcn0x7iznoVTkg6kzthl6w-gzGzoHsz", "cTNJGjdsCK6snzqmNhTsumjp")

leancloud.init("Fhdcn0x7iznoVTkg6kzthl6w-gzGzoHsz", master_key="usMoq9bILw9Yp39lL2K89sjq")



class _File(Object):
    pass

class Todo(Object):
    pass

class _User(Object):
    pass

class Project(Object):
    pass

class ProjectDate(Object):
    pass

class StatDAU(Object):
    pass

class StatLog(Object):
    pass

class StatUser(Object):
    pass

class UserProjectMap(Object):
    pass

class StatInternalUser(Object):
    pass    

if len(sys.argv) != 2:
    print("argv error !!!")
    exit(1)

del_range = sys.argv[1]
exp_ip_col = "("

if del_range == "all":
    cql_get_exp_ip = "select objectId, androidId from StatInternalUser limit 99999999"
    todo_query_exp_ip = leancloud.Query.do_cloud_query(cql_get_exp_ip)
    todo_list_exp_ip = todo_query_exp_ip.results # 返回符合条件的 todo list 
    if todo_list_exp_ip != []:
        for each_exp_ip in todo_list_exp_ip:
            exp_ip_col = exp_ip_col + "'" + each_exp_ip.get('androidId') + "'," 
    exp_ip_col = exp_ip_col[:-1] +")"
else:
    exp_ip_col = exp_ip_col + "'" + del_range + "')"


### deleting items from StatUser
print("Checking StatUser ...\r\n")
cql_update_items = "select objectId, projectId , androidId from StatUser where androidId in " + exp_ip_col
print(cql_update_items)
todo_query_update_items = leancloud.Query.do_cloud_query(cql_update_items)
todo_update_items = todo_query_update_items.results # 返回符合条件的 todo list 

oid_pid = []
oid_str = "("
if todo_update_items ==[]:
    print('No item to delete !!! in StatUser\r\n')
    oid_str = "()"
    # exit(0)

else:
    print("Deleting items from StatUser ... \r\n")
    try:
        for each_del_item in todo_update_items:
            dic = {}
            dic['oid'] = each_del_item.get('objectId')
            dic['pid'] = each_del_item.get('projectId')
            dic['aid'] = each_del_item.get('androidId')
            oid_pid.append(dic)
            oid_str = oid_str + "'" + each_del_item.get('objectId') + "',"  
        oid_str = oid_str[:-1] + ")"
        for each_oidpid in oid_pid:
            # if each_oidpid['pid'].count("del_del_") > 0:
            #     pid_tobe = each_oidpid['pid'].replace("del_del_","del_")
            if each_oidpid['pid'].count("del_") == 0:
                now = datetime.datetime.now()
                date_str = now.strftime('%Y%m%d_%H%M%S_')                 
                pid_tobe = "del_" + date_str + each_oidpid['pid']
                cql_update_items_II = "update StatUser set projectId = '" + pid_tobe + "' where objectId = '" + each_oidpid['oid'] + "'"
                # print(cql_update_items_II)
                todo_query_update_items_II = leancloud.Query.do_cloud_query(cql_update_items_II)
                todo_update_items_II = todo_query_update_items_II.results # 返回符合条件的 todo list
                msg_each_update = "StatUser item deleted !!! android id : " + dic['aid']
                print(msg_each_update) 
        print("Completed !!!\r\n")
    except Exception, e:  
        print(str(e))
        exit(1)  
###

### deleting items from StatDAU
print("Checking StatDAU ...\r\n")
cql_get_DAU_oid = "select objectId, projectId from StatDAU where userId in " + oid_str
# print(cql_get_DAU_oid)
todo_query_get_DAU_oid = leancloud.Query.do_cloud_query(cql_get_DAU_oid)
todo_get_DAU_oid = todo_query_get_DAU_oid.results # 返回符合条件的 todo list 

oid_pid_DAU = []
if todo_get_DAU_oid ==[]:
    print('No item to delete !!!\r\n')
    exit(0)
else:
    print("Deleting items from StatDAU ... \r\n")
    try:
        for each_DAU_oid in todo_get_DAU_oid:
            dic = {}
            dic['oid'] = each_DAU_oid.get('objectId')
            dic['pid'] = each_DAU_oid.get('projectId')
            # dic['aid'] = each_del_item.get('androidId')
            oid_pid_DAU.append(dic)

        for each_oidpid_DAU in oid_pid_DAU:
            if each_oidpid_DAU['pid'].count("del_") == 0:
                now = datetime.datetime.now()
                date_str = now.strftime('%Y%m%d_%H%M%S_')                  
                pid_tobe_DAU = "del_" + date_str + each_oidpid_DAU['pid']
                cql_get_DAU_oid_II = "update StatDAU set projectId = '" + pid_tobe_DAU + "' where objectId = '" + each_oidpid_DAU['oid'] + "'"
                todo_query_get_DAU_oid_II = leancloud.Query.do_cloud_query(cql_get_DAU_oid_II)
                todo_get_DAU_oid_II = todo_query_get_DAU_oid_II.results # 返回符合条件的 todo list 
                msg_each_update = "StatDAU item deleted !!! User id : " + dic['oid']
                print(msg_each_update)                 
    except Exception, e:  
        print(str(e))
        exit(1)  
    print("Completed !!!")
###


