#!/usr/bin/python

import CloudStack

api='https://api.ucloudbiz.olleh.com/server/v1/client/api'
apikey='API KEY'
secret='SECRET KEY'

cloudstack = CloudStack.Client(api, apikey, secret)

import base64
#userdata=base64.b64encode("#!/bin/bash\necho \"127.0.0.1 $(hostname)\" >> /etc/hosts\ntouch /root/file-from-userdata")

rawuserdata='''#!/bin/sh
logger -t "cloud" "USERDATA START"

cp /tmp/userdata /root/userdata
mkdir -p /DATA/script
cd /DATA/script
/usr/bin/wget https://s3.amazonaws.com/ngsbench/userscript.py
chmod 755 /DATA/script/userscript.py
/usr/bin/python userscript.py
cp /tmp/userdata.log /root/userdata.log

logger -t "cloud" "STEP 1 fin"

/usr/bin/apt-get install -y python-pip
/usr/bin/pip install boto

logger -t "cloud" "STEP 2 fin"

/usr/bin/python -c "import boto
sns=boto.connect_sns(aws_access_key_id='AWS Access Key', aws_secret_access_key='AWS Secret Key')
sns.publish('arn:aws:sns:us-east-1:263049782498:paws_cloudwatch','u r geninus','USER DATA FIN')
"

logger -t "cloud" "STEP 3 fin"
logger -t "cloud" "USERDATA END"
'''

userdata=base64.b64encode(rawuserdata)

#print rawuserdata
print userdata

print "Now Deploy Virtual Machine (A)"
job=cloudstack.deployVirtualMachine({
   'serviceofferingid':'131',
   'templateid':'932',
   'diskofferingid':'130',
   'zoneid':'2',
   'domainid':'8',
   'displayname':'HONGIIV',
   'userdata':userdata
})

print "VM being deployed.job id =%s"%job['jobid']
print "My VM ID: %s"%(job['id'])
vmid = job['id']


import time

myjob = job['jobid']

while True:
   qr=cloudstack.queryAsyncJobResult({
      'jobid':str(myjob)
   })
   if qr['jobstatus'] == 1:
      print "Job Success"
      break
   elif qr['jobstatus'] == 2:
      print "Job fail"
      break
   else:
      print qr['jobstatus']
      print "Sleep"
      time.sleep(5)
   
print "Fin"

print "Now Reboot Virtual Machine (A)"
job=cloudstack.resetPasswordForVirtualMachine({
   'id':str(vmid)
})

myjob=job['jobid']

while True:
   qr=cloudstack.queryAsyncJobResult({
      'jobid':str(myjob)
   })
   if qr['jobstatus'] == 1:
      print "Password Reset Job Success\n"
      print qr
      break
   elif qr['jobstatus'] == 2:
      print "Job fail"
      break
   else:
      print qr['jobstatus']
      print "Sleep"
      time.sleep(5)
  
print "Fin"
