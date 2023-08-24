from LogAppRestClientLibrary.RequestHandlers.IRequestHandler import IRequestHandler
from LogAppRestClientLibrary.Environment import Env
from Endpoints.ConfigurationGroup import ConfigurationGroup

env = Env()

class LogAgent():
    requestHandler: IRequestHandler
    listOfConfigGroups = []

    def __init__(self, id) -> None:
        self.id = id
        self.path = ""
        data = self.loadData(self.id)
        if data:
            self.data = data

    def __str__(self):
        return f"LogAgent:{self.data}"

    def loadData(self, id):
        url = env.url + "logagents/" + str(self.id)
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    @staticmethod
    def GetLogAgents():
        url = env.url + "logagents"
        return env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify)

    def save(self):
        url = env.url + "logagents/" + str(self.id)
        return env.requestHandler.PUT(url=url, headers=env.headers, verify=env.verify, data=self.data)

    def delete(self):
        url = env.url + "logagents/" + str(self.id)
        return env.requestHandler.DELETE(url=url, headers=env.headers, verify=env.verify)

    def getAssignedConfigurationGroups(self):
        if(self.listOfConfigGroups == []):
            url = env.url + "logagents/" + str(self.id) + "/assigned-configurationgroups"
            for configgroup in env.requestHandler.GET(url=url, headers=env.headers, verify=env.verify):
                self.listOfConfigGroups.append(ConfigurationGroup(configgroup['id']))
        return self.listOfConfigGroups

    def assignConfigurationGroup(self, configGroupID):
        url = env.url + "logagents/" + str(self.id) + "/assigned-configurationgroups/" + str(configGroupID)
        return env.requestHandler.PUT(url=url, headers=env.headers, verify=env.verify)

    def removeConfigurationGroup(self, configGroupID):
        url = env.url + "logagents/" + str(self.id) + "/assigned-configurationgroups/" + str(configGroupID)
        return env.requestHandler.DELETE(url=url, headers=env.headers, verify=env.verify)

    @staticmethod
    def getInstallerByType(typeOfInstaller):
        url = env.url + f"logagent-installers/{typeOfInstaller}"
        return env.requestHandler.GETPATH(url=url, headers=env.headers, verify=env.verify)
        
    @staticmethod
    def getWindowsServerAgentInstaller(path = ""):
        with open(f"{path}WindowsServerAgentInstaller.zip", "wb") as file:
            file.write(LogAgent.getInstallerByType(1))
        return True

    @staticmethod
    def getWindowsClientAgentInstaller(path = ""):
        with open(f"{path}WindowsClientAgentInstaller.zip", "wb") as file:
            file.write(LogAgent.getInstallerByType(2))
        return True
    @staticmethod
    def getUbuntuAgentInstaller(path = ""):
        with open(f"{path}UbuntuAgentInstaller.tar.gz", "wb") as file:
            file.write(LogAgent.getInstallerByType(3))
        return True

    @staticmethod
    def getCentosRhelAgentInstaller(path = ""):
        with open(f"{path}CentosRhelAgentInstaller.tar.gz", "wb") as file:
            file.write(LogAgent.getInstallerByType(4))
        return True

    @staticmethod
    def getAixAgentInstaller(path = ""):
        with open(f"{path}AixAgentInstaller.tar.gz", "wb") as file:
            file.write(LogAgent.getInstallerByType(5))
        return True

    @staticmethod
    def getDefaultCertificateWindows(path = ""):
        with open(f"{path}DefaultCertificateWindows.zip", "wb") as file:
            file.write(LogAgent.getInstallerByType(6))
        return True

    @staticmethod
    def getDefaultCertificateLinux(path = ""):
        with open(f"{path}DefaultCertificateLinux.tar.gz", "wb") as file:
            file.write(LogAgent.getInstallerByType(7))
        return True