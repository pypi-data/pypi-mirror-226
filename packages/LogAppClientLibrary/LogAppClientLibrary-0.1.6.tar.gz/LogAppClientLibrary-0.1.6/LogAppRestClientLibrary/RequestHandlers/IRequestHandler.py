from abc import ABC, abstractmethod
class IRequestHandler(ABC):
    @abstractmethod
    def loadData(self):
        pass
    @abstractmethod
    def GET(self,**kwargs):
        pass
    @abstractmethod
    def PUT(self,**kwargs):
        pass
    @abstractmethod
    def DELETE(self,**kwargs):
        pass
    @abstractmethod
    def POST(self,**kwargs):
        pass
