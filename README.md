CloudStack Python Client for ucloud biz
==========================================

본 API는 CloudStack User API v3.0.0을 위한 Python 라이브러리이며, KT의 uclod biz 상품을 이용하기 위한 몇몇 기능이 추가된 버전으로, Jason Hancock <jsnbyh@gmail.com>의 Python Client를 기반으로 하고 있습니다.

Examples
--------

ucloud biz에 생성된 모든 vm의 목록 조회

```python
#!/usr/bin/python

import CloudStack

api='https://api.ucloudbiz.olleh.com/server/v1/client/api'
apikey='Your API KEY'
secret='Your SECRET KEY'

cloudstack = CloudStack.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

print "VmID\tName\tState\taccount\tdomian\tdomainid\tPassword"

for vm in vms:
    print "%s\t%s\t%s\t%s\t%s\t%s" % (vm['id'], vm['name'], vm['account'], vm['domain'], vm['domainid'], vm['state'])

```

ucloud biz에서 사용 가능한 모든 상품의 목록 조회

```python
#!/usr/bin/python

import CloudStack

api='https://api.ucloudbiz.olleh.com/server/v1/client/api'
apikey='Your API KEY'
secret='Your SECRET KEY'
cloudstack = CloudStack.Client(api, apikey, secret)

products = cloudstack.listAvailableProductTypes()
print "============================================================================================================="
print "ProductID\tServiceOfferingID\tDesc\tTemplateID\tDesc\tDiskOfferingID\tDesc\tAvailable\tzoneid"
print "============================================================================================================="
for product in products['producttypes']:
    if product['templatedesc'] == "Ubuntu 11.04 64bit":
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(product['productid'],product['serviceofferingid'],product['serviceofferingdesc'],product['templateid'],product['templatedesc'],product['diskofferingid'],product['diskofferingdesc'],product['productstate'],product['zoneid'])
    else:
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(product['productid'],product['serviceofferingid'],product['serviceofferingdesc'],product['templateid'],product['templatedesc'],product['diskofferingid'],product['diskofferingdesc'],product['productstate'],product['zoneid'])

```

Asynchronous tasks

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

job = cloudstack.deployVirtualMachine({
    'serviceofferingid': '2',
    'templateid':        '214',
    'zoneid':            '2'
})

print "VM being deployed. Job id = %s" % job['jobid']

print "All Jobs:"
jobs = cloudstack.listAsyncJobs({})
for job in jobs:
    print  "%s : %s, status = %s" % (job['jobid'], job['cmd'], job['jobstatus'])

```

TODO:
-----
There is a lot to do to clean up the code and make it worthy of production. This
was just a rough first pass.
