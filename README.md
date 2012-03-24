CloudStack Python Client for ucloud biz
==========================================

본 API는 CloudStack User API v3.3.3을 위한 Python 라이브러리이며, Jason Hancock <jsnbyh@gmail.com>의 Python Client를 기반으로 제작되었습니다.

Python client library for the CloudStack User API v3.0.0. For older versions,
see the [tags](https://github.com/jasonhancock/cloudstack-python-client/tags).

Examples
--------

List all virtual machines

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

for vm in vms:
    print "%s %s %s" % (vm['id'], vm['name'], vm['state'])
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
