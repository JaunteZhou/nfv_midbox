import json
import urllib2

root_uri = 'http://192.168.1.68:5000'

def curl_keystone():  
    auth_uri = '/v3/auth/tokens'
    values = {
                "auth": {
                    "identity": {
                        "methods": [
                            "password"
                        ],
                        "password": {
                            "user": {
                                "name": "admin",
                                "domain": {
                                    "name": "Default"
                                },
                                "password": "openstack"
                            }
                        }
                    }
                }
            }
    auth_params = json.dumps(values)
    print(auth_params)

    headers = {"Content-type":"application/json","Accept": "application/json"}
    auth_req = urllib2.Request(root_uri + auth_uri, auth_params, headers)
    auth_response = urllib2.urlopen(auth_req)
    raw_data = auth_response.read()
    json_data = json.loads(raw_data)
    print(json_data)

    #token = json_data['access']['token']['id']  
    # return token


    # date=auth_response.getheader('date');
    # print("Data:")
    # print(date)
    # resheader=''
    resheader=auth_response.info();
    print("X-Subject-Token:")
    token = resheader['X-Subject-Token']
    print(resheader['X-Subject-Token'])
    return resheader

    

# def curl_nova_addr(id):  
#     """
#        :param id: vm id  
#        :Restore vm ip address.  
#     """
#     xtoken = curl_keystone()  
#     url = 'http://192.168.12.1:8774/v2/2996e46c2519415d8de2b141d6c607ba/servers/'+id  
#     headers = {"Content-type":"application/json","Accept": "application/json"}  
#     req = urllib2.Request(url)  
#     req.add_header('X-Auth-Token',xtoken)  
#     response = urllib2.urlopen(req)  
#     data = response.read()  
#     ddata=json.loads(data)  
#     net = ddata['server']['addresses']['sharednet1']  
#     addr = net[0]['addr']  
#     return addr  

# def curl_nova_id(name):  
#     """
#        :param name: Something to name the server.  
#        :Restore vm id.  
#     """
#     ID=""
#     xtoken = curl_keystone()  
#     url = 'http://192.168.12.1:8774/v2/2996e46c2519415d8de2b141d6c607ba/servers'  
#     headers = {"Content-type":"application/json","Accept": "application/json"}  
#     req = urllib2.Request(url)  
#     req.add_header('X-Auth-Token',xtoken)  
#     response = urllib2.urlopen(req)  
#     data = response.read()  
#     ddata=json.loads(data)  
#     list=ddata['servers']  
#     print len(list)  
#     print list  
#     for i in list:  
#        if(i['name'] == name):  
#            ID= i['id']  
#     return ID 


key = curl_keystone()

print(key)


#{"auth": {"identity": {"methods": ["password"],"password": {"user": {"name": "admin","domain": {"name": "Default"},"password": "devstacker"}}}}}