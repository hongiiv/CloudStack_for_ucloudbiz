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
            errorcode = str(e.code)
            errortext = e.read()
            print 'Error>>> Error code:', errorcode

            if errorcode == '502':
               print '502 error handling'
               #errortext = "{u'deployvirtualmachineresponse': {u'errorcode': u'502', u'errortext': u'The proxy server received an invalid response'}}"
               errortext = '{"defaultresponse": {"errorcode": "502", "errortext": "The proxy server received an invalid response"}}'
               print errortext
               decoded = json.loads(errortext)
               print decoded
               propertyResponse = command.lower() + 'response'
               print propertyResponse
               response = decoded['defaultresponse']
               print response
               return response
            elif errorcode == '500':
               print '500 error handling'
               errortext = '{"defaultresponse": {"errorcode": "500", "errortext": "?????"}}'
               print errortext
               decoded = json.loads(errortext)
               print decoded
               propertyResponse = command.lower() + 'response'
               print propertyResponse
               response = decoded['defaultresponse']
               print response
               return response
            elif errorcode == '503':
               print '503 error handling'
               errortext = '{"defaultresponse": {"errorcode": "503", "errortext": "Excessive traffic error"}}'
               print errortext
               decoded = json.loads(errortext)
               print decoded
               propertyResponse = command.lower() + 'response'
               print propertyResponse
               response = decoded['defaultresponse']
               print response
               return response

            else:
               decoded = json.loads(errortext)
               print '>>>>>>>>>>>>>>>'
               print decoded
               propertyResponse = command.lower() + 'response'
               ###print "propertyResponse: "
               ###print propertyResponse
               response = decoded[propertyResponse]
               #response = decoded['defaultresponse']
               ###print response
               return response
        except URLError, e:
            print 'We failed to reach a server.'
            #print 'Reason:', e.reason
            #errortext = "{u'defaultresponse': {u'errorcode': u'000', u'errortext': u'failed to reach a server'}}"
            errortext = '{"defaultresponse": {"errorcode": "999", "errortext": "failed to reach a server"}}'
            print errortext
            decoded = json.loads(errortext)
            print decoded
            propertyResponse = command.lower() + 'response'
            print propertyResponse
            #response = decoded[propertyResponse]
            response = decoded['defaultresponse']
            print response
            return response
        else:
            decoded = json.loads(response.read())
       
            '''
            if command == 'listAvailableProductTypes':
                propertyResponse = command + 'response'
            else:
                propertyResponse = command.lower() + 'response'
            print command
            '''
            propertyResponse = command.lower() + 'response'
            ###print command

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
