from LogAppRestClientLibrary.RequestHandlers.IRequestHandler import IRequestHandler
import requests

class RealRequest(IRequestHandler):
    def loadData(self):
        pass
    def GET(self,**kwargs):
        response = requests.get(url=kwargs['url'],headers=kwargs['headers'],verify=kwargs['verify'])
        print(response.content)
        if response.status_code == 200:
            return response.json()  
        else:
            print("Request failed with status code:", response.status_code)
        return None
    def PUT(self,**kwargs):
        response = requests.put(url=kwargs['url'],headers=kwargs['headers'],verify=kwargs['verify'],json=kwargs['data'])
        if response.status_code == 200:  
            return True
        else:
            print("Request failed with status code:", response.status_code)
        return None
    def DELETE(self,**kwargs):
        response = requests.delete(url=kwargs['url'],headers=kwargs['headers'],verify=kwargs['verify'])
        if response.status_code == 200:  
            return True
        else:
            print("Request failed with status code:", response.status_code)
        return None
    def POST(self,**kwargs):
        response = requests.post(url=kwargs['url'],headers=kwargs['headers'],verify=kwargs['verify'],json=kwargs['data'])
        if response.status_code == 200:  
            return True
        else:
            print("Request failed with status code:", response.status_code)
        return None
    def GETPATH(self,**kwargs):
        response = requests.get(url=kwargs['url'],headers=kwargs['headers'],verify=kwargs['verify'])
        if response.status_code == 200:
            return response.content  
        else:
            print("Request failed with status code:", response.status_code)
        return None