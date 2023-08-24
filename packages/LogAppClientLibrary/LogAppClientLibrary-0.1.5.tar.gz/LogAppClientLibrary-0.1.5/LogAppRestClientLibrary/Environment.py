from RequestHandlers.Real_request import RealRequest
class Env():
    def __init__(self) -> None:
        self.host = "https://10.100.181.240"
        self.port = "8080"
        self.url = self.host + ":"+self.port+"/"
        self.bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJDbGllbnRfSUQiOiIxIiwiQWNjZXNzIjoiZUZudmdBT0NvZjB5em1zUXZ4WjcifQ.9J6_xKNG-6L_RnJS7Woq20BZRZpUboBMQknSX7E0YJE"
        self.headers = {
        "Authorization": "Bearer "+self.bearer
        }
        self.verify = False
        self.requestHandler=RealRequest()

