import json
import urllib2



class OpenStackSocket(object):
    def __init__(self, root_url = 'http://192.168.1.68'):
        self.root_url = root_url
        self.auth_port = '5000'
        self.compute_port = '8778'
        self.token = ''
        self.name_val = ''
        self.domain_val = ''
        self.pwd_val = ''

    def set_auth_info(
            self, 
            name_val = '', 
            domain_val = '', 
            pwd_val = ''
            ):
        self.name_val = name_val
        self.domain_val = domain_val
        self.pwd_val = pwd_val

    def get_auth_info(self):
        return {"name":self.name_val, "domain":self.domain_val}

    def get_token_from_keystone(self):
        auth_uri = '/v3/auth/tokens'
        auth_values = {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "name": self.name_val,
                                "domain": {
                                    "name": self.domain_val
                                },
                                "password": self.pwd_val
                            }
                        }
                    }
                }
            }
        auth_params = json.dumps(auth_values)
        headers = {"Content-type":"application/json","Accept": "application/json"}

        auth_req = urllib2.Request(
            self.root_url + ':' + self.auth_port + auth_uri, auth_params, headers)
        auth_response = urllib2.urlopen(auth_req)

        self.token = auth_response.info()['X-Subject-Token']
        # print(self.token)

        return json.loads(auth_response.read())

    def get_servers_list(self):
        compute_uri = '/flavors'
        headers = {
                "Content-type":"application/json",
                "Accept": "application/json"
            }
        values = {}
        params = json.dumps(values)
        req = urllib2.Request(self.root_url + ':' + self.compute_port + compute_uri)
        req.add_header('X-Auth-Token', self.token)
        res = urllib2.urlopen(req)
        data = response.read()  
        return data

    def curl_nova_addr(self, id):  
        """  
           :param id: vm id  
           :Restore vm ip address.  
        """  
        xtoken = curl_keystone()  
        url = 'http://192.168.12.1:8774/v2/2996e46c2519415d8de2b141d6c607ba/servers/'+id  
        headers = {"Content-type":"application/json","Accept": "application/json"}  
        req = urllib2.Request(url)  
        req.add_header('X-Auth-Token',xtoken)  
        response = urllib2.urlopen(req)  
        data = response.read()  
        ddata=json.loads(data)  
        net = ddata['server']['addresses']['sharednet1']  
        addr = net[0]['addr']  
        return addr

    def curl_nova_id(self, name):  
        """  
           :param name: Something to name the server.  
           :Restore vm id.  
        """  
        ID=""  
        xtoken = curl_keystone()  
        url = 'http://192.168.12.1:8774/v2/2996e46c2519415d8de2b141d6c607ba/servers'  
        headers = {"Content-type":"application/json","Accept": "application/json"}  
        req = urllib2.Request(url)  
        req.add_header('X-Auth-Token',xtoken)  
        response = urllib2.urlopen(req)  
        data = response.read()  
        ddata=json.loads(data)  
        list=ddata['servers']  
        print len(list)  
        print list  
        for i in list:  
           if(i['name'] == name):  
               ID= i['id']  
        return ID 

if __name__ == "__main__":
    oss = OpenStackSocket()
    oss.set_auth_info("admin", "Default", "openstack")
    print(oss.get_auth_info())

    res = oss.get_token_from_keystone()
    print(res)
    print(oss.token)
    # servers = oss.get_servers_list()
    # print(servers)
    # print(res['token']['issued_at'])
