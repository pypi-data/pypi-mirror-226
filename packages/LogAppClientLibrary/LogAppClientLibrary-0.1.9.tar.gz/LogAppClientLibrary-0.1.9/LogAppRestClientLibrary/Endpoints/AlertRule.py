from LogAppRestClientLibrary.RequestHandlers.IRequestHandler import IRequestHandler
from LogAppRestClientLibrary.Environment import Env
from Endpoints.ConfigurationGroup import ConfigurationGroup

env = Env()
class AlertRule():
    requestHandler: IRequestHandler

    def __init__(self, _id) -> None:
        self.id = _id
        data = self.loadData(self.id)
        if data:
            self.data = data

    def loadData(self, _id):
        url = env.url + "alertrules/" + str(self.id)
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    @staticmethod
    def GetAlertRules(parameters=None):
        url = env.url + "alertrules"
        if parameters:
            url += "?" + "&".join([f"{key}={value}" for key, value in parameters.items()])
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    def save(self):
        url = env.url + "alertrules/" + str(self.id)
        return env.requestHandler.PUT(url=url, headers=env.headers, verify=env.verify, data=self.data)

    def disable(self):
        self.data['enabled'] = False
        self.save()

    def enable(self):
        self.data['enabled'] = True
        self.save()

    def delete(self):
        url = env.url + "alertrules/" + str(self.id)
        return env.requestHandler.DELETE(url=url, headers=env.headers, verify=env.verify)

