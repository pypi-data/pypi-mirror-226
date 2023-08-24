from LogAppRestClientLibrary.RequestHandlers.IRequestHandler import IRequestHandler
from LogAppRestClientLibrary.Environment import Env
env = Env()
class ConfigurationGroup():
    requestHandler: IRequestHandler

    def __init__(self, _id) -> None:
        self.id = _id
        data = self.loadData(self.id)
        if data:
            self.data = data
    def __str__(self) -> str:
        return f"id:{self.data['id']} name: {self.data['name']} type: {self.data['type']}"

    def loadData(self, _id):
        url = env.url + "configurationgroups/" + str(self.id)
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    @staticmethod
    def GetConfigurationGroups(parameters=None):
        url = env.url + "configurationgroups"
        if parameters:
            url += "?" + "&".join([f"{key}={value}" for key, value in parameters.items()])
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    def save(self):
        url = env.url + "configurationgroups/" + str(self.id)
        return env.requestHandler.PUT(url=url, headers=env.headers, verify=env.verify, data=self.data)

    def delete(self):
        url = env.url + "configurationgroups/" + str(self.id)
        return env.requestHandler.DELETE(url=url, headers=env.headers, verify=env.verify)