from LogAppRestClientLibrary.Environment import Env
from LogAppRestClientLibrary.RequestHandlers.IRequestHandler import IRequestHandler
env = Env()

class Alert():
    requestHandler : IRequestHandler
    def __init__(self, id) -> None:
        self.id = id
        data = self.loadData(self.id)
        if data:
            self.data = data; 

    def __str__(self):
        return f"Alert: {self.data['alertName']}\nMessage: {self.data['alertMessage']}\nRule: {self.data['alertRule']}\nPriority: {self.data['priority']}\nStatus: {self.data['status']}"
    def loadData(self, id):
        url = env.url+"alerts/"+ str(self.id)
        return env.requestHandler.GET(url = url, headers=env.headers, verify=env.verify)
    
    @staticmethod
    def GetAlerts(parameters=None):
        url = env.url + "alerts"
        if parameters:
            url += "?" + "&".join([f"{key}={value}" for key, value in parameters.items()])
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)
    
    def save(self):
        url = env.url+"alerts/"+str(self.id)
        return env.requestHandler.PUT(url = url,headers = env.headers,verify =env.verify,data=self.data)
    def close(self):
        self.status = "Resolved"
        self.data['status'] = "Resolved"
        self.save()
    def getEventsToAlert(self):
        url = env.url +"alerts/"+str(self.id) + "/events-of-alert"
        return env.requestHandler.GET(url = url, headers=env.headers, verify=env.verify)