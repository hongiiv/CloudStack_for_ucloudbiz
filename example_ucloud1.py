#!/usr/bin/python

import ucloudapi

api='https://api.ucloudbiz.olleh.com/server/v1/client/api'
apikey='APIKEY'
secret='SECRETKEY'

cloudstack = ucloudapi.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

print "VmID\tName\tState\taccount\tdomian\tdomainid\tPassword"

for vm in vms:
    print "%s\t%s\t%s\t%s\t%s\t%s" % (vm['id'], vm['name'], vm['account'], vm['domain'], vm['domainid'], vm['state'])

print

products = cloudstack.listAvailableProductTypes()
print "============================================================================================================="
print "ProductID\tServiceOfferingID\tDesc\tTemplateID\tDesc\tDiskOfferingID\tDesc\tAvailable\tzoneid"
print "============================================================================================================="
for product in products['producttypes']:
    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(product['productid'],product['serviceofferingid'],product['serviceofferingdesc'],product['templateid'],product['templatedesc'],product['diskofferingid'],product['diskofferingdesc'],product['productstate'],product['zoneid'])

print

lvols=cloudstack.listVolumes()
print "============================================================================================================="
print "virtualmachineid\tvmname\tname\tsize\ttype\t"
print "============================================================================================================="
for lvol in lvols:
   if lvol.has_key('virtualmachineid'):
      print "%s\t%s\t%s\t%s\t%s"%(lvol['virtualmachineid'],lvol['vmname'],lvol['name'],lvol['size'],lvol['type'])
   else:
      print "null\tnull\t%s\t%s\t%s"%(lvol['name'],lvol['size'],lvol['type'])

print

ports=cloudstack.listPortForwardingRules()
print "============================================================================================================="
print "ruleid\tipaddress\tipaddressid\tprotocol\tprivateend\tpublicend\tvmid"
print "============================================================================================================="
for port in ports:
   print "%s\t%s\t%s\t%s\t%s\t%s\t%s"%(port['id'],port['ipaddress'],port['ipaddressid'],port['protocol'],port['privateendport'],port['publicendport'],port['virtualmachineid']) 
 

'''
vols=cloudstack.createVolume({
   'name':'biotest',
   'diskofferingid':'140',
   'zoneid':'2',
   'account':'bio1',
   'domainid':'8'
})

myjob=vols['id']

while True:
   qr=cloudstack.queryAsyncJobResult({
      'jobid':str(myjob)
   })
   if qr['jobstatus'] == 1:
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
'''
