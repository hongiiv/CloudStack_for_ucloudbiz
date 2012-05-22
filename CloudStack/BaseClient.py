import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import json
import hmac
import base64
import hashlib
import re

class BaseClient(object):
    def __init__(self, api, apikey, secret):
        self.api = api
        self.apikey = apikey
        self.secret = secret

    def request(self, command, args):
        args['apikey']   = self.apikey
        args['command']  = command
        args['response'] = 'json'
        
        params=[]
        
        keys = sorted(args.keys())

        for k in keys:
            params.append(k + '=' + urllib.quote_plus(args[k])) 
       
        query = '&'.join(params)

        signature = base64.b64encode(hmac.new(
            self.secret, 
            msg=query.lower(), 
            digestmod=hashlib.sha1
        ).digest())

        query += '&signature=' + urllib.quote_plus(signature)

        #hongiiv
        print self.api+'?'+query

        try:
            response = urllib2.urlopen(self.api + '?' + query)
        except HTTPError, e:
            print 'Error>>> The server couldn\'t fulfill the request.'
            print 'Error>>> Error code:', e.code
            print 'Error>>>', e.read()
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason:', e.reason
        else:
            decoded = json.loads(response.read())
       
            if command == 'listAvailableProductTypes':
                propertyResponse = command + 'response'
            else:
                propertyResponse = command.lower() + 'response'
            print command

            if not propertyResponse in decoded:
                if 'errorresponse' in decoded:
                    raise RuntimeError("ERROR: " + decoded['errorresponse']['errortext'])
                else:
                    raise RuntimeError("ERROR: Unable to parse the response")

            response = decoded[propertyResponse]
            result = re.compile(r"^list(\w+)s").match(command.lower())

            if not result is None:
                type = result.group(1)

                if type in response:
                    return response[type]
                else:
                    # sometimes, the 's' is kept, as in :
                    # { "listasyncjobsresponse" : { "asyncjobs" : [ ... ] } }
                    type += 's'
                    if type in response:
                        return response[type]

            return response
