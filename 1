import CloudStack
import pexpect
import time
import os
import json
import boto
from uuid import uuid4
import thread
from boto.sqs.message import Message
import sqlite3

REQUEST_QUEUE = 'developer'
MAX_TRY = 10 #if failed deploy virtual machine we will try 10 times
VISIBILITY_TIMEOUT = 600 # 10 min
KT_HOST = 'https://api.ucloudbiz.olleh.com/server/v1/client/api'
KT_APIKEY = 'iW59r_QY7T07T-fXY7FH8IRsYbgJ6b-fV4pvCFsYkbx6ArMGFhaL4-sEz7zbpCNUA1I6ovcLIH2dTbXVp34mAA'
KT_SECRET = 'ttteX3ygXMJBHPinj3zVOuHg1WCq3tqX014elUPkMryMhiGP3OjcBijKPkMA7N9DGCZY5RvO9aLMuOh6SfY9dQ'
SQLITE_ADMIN = 'genome_admin'

def update_db(n_date,displayname,code):
   while(1):
      db = sqlite3.connect(SQLITE_ADMIN)
      cursor = db.cursor()
      print ">>>>>>>>>>>>>"
      datas = (code, n_date, displayname)
      SQL = "update genome_admin set status_code='%s', date_process_start='%s' where displayname='%s'"%(code,n_date,displayname)
      print SQL
      try:
         cursor.execute(SQL)
         #cursor.execute("update genome_admin set (status_code=?, date_process_start=?) where displayname=?", datas) 
         cursor.close()
         db.commit()
         db.close()
         print "Successfully updated db"
         break
      except sqlite.OperationalError:
         print "database locked"

def launch_vm(m):
   cloudstack = CloudStack.Client(KT_HOST, KT_APIKEY, KT_SECRET)
   message_data = json.loads(m.get_body())

   now = time.localtime()
   #now_date = "%02d-%02d-%02d" % (now.tm_mday, now.tm_hour, now.tm_min)
   now_date = "%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

   #db_update/message_update
   update_db(now_date, message_data['displayname'],"101")

   reservation = cloudstack.deployVirtualMachine({
      'serviceofferingid': message_data['serviceofferingid'],
      'templateid': message_data['templateid'],
      'diskofferingid':message_data['diskofferingid'],
      'zoneid':message_data['zoneid'],
      'usageplantype':message_data['usageplantype'],
      'displayname': message_data['displayname'],
   })
 
   if reservation.has_key('errorcode'):
      print '>>>error during resource reservation, deployvirtualmachine %s >> 501'%(message_data['displayname'])
      #db_update/message_update
      now = time.localtime()
      now_date = "%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
      update_db(now_date,message_data['displayname'],"501")
      #this message will be apeared 1 hour later
      print '[deployvirtualmachine] Resquest fail / message will be back : %s %s'%(reservation['errorcode'],reservation['errortext'])
      result ='{"rescode":"2"}'
   else:
      jobid = reservation['jobid']
      vmid = reservation['id']
      #db_update/message_update
      now = time.localtime()
      now_date = "%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
      update_db(now_date,message_data['displayname'],"102")

      while True:
         asyncstatus = cloudstack.queryAsyncJobResult({
            'jobid':jobid
         })

         if asyncstatus.has_key('errorcode'):
            print '[asyncstatus_error01] Resquest fail but i love u: %s %s'%(asyncstatus['errorcode'],asyncstatus['errortext'])
            time.sleep(5)
         elif asyncstatus['jobstatus'] == 1:
            password = asyncstatus['jobresult']['virtualmachine']['password']
            ipaddress = asyncstatus['jobresult']['virtualmachine']['nic'][0]['ipaddress']
            print "[deployvirtualmachine] VM was successfuly created %s %s"%(ipaddress, password)
            result ='{"rescode":"1","ipaddress": "%s","password":"%s"}'%(ipaddress,password)

            #db_update/message_update
            now = time.localtime()
            #now_date = "%02d-%02d-%02d" % (now.tm_mday, now.tm_hour, now.tm_min)
            now_date = "%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            update_db(now_date,message_data['displayname'],"103")
            break
         elif asyncstatus['jobstatus'] == 2:
            result ='{"rescode":"2"}'
            #db_update/message_update
            print '[asyncstatus_error02] job file'
            now = time.localtime()
            now_date = "%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            update_db(now_date,message_data['displayname'],"502")
            break
         else:
            print '.'
            time.sleep(5)

   print 'done'
   return result

def read_queue():
   sqs_conn = boto.connect_sqs()
   request_queue = sqs_conn.create_queue('developer')
   message = request_queue.read(VISIBILITY_TIMEOUT) #3600 sec, 1 hour
   if message is not None:
      #data = json.loads(message.get_body())
      #data = message.get_body()
      print "I receive the message, read it"
      run(message)
   else:
      print "I havn't message, Give me a message :)"
   
def run(message):
   try_count = 0
   while True:
      if try_count != MAX_TRY:
         launch_result = launch_vm(message)
         #print launch_result
         result = json.loads(launch_result)
         if result['rescode'] == '1':
            sqs_conn = boto.connect_sqs()
            request_queue = sqs_conn.create_queue(REQUEST_QUEUE)
            request_queue.delete_message(message)
            print "Delete message from dev queue :("
            return 1
            break
         elif result['rescode'] == '2':
            print 'job fail'
            try_count = try_count +1
      else:
         print try_count
         print "last job fail"
         sqs_conn = boto.connect_sqs()
         request_queue = sqs_conn.create_queue(REQUEST_QUEUE)
         request_queue.delete_message(m)
         new_m = Message()
         new_m.set_body('new')
         status = request_queue.write(new_m)
         print "Re-insert queue message (fail) :(" 
         return 2
         break

#if __name__ == "__main__":
while True:
   thread.start_new_thread(read_queue,())
   print "I will read a queue"
   time.sleep(5)
