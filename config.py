import json

CONCURRENT_REQUESTS = 2

class TestConfig:
    def __init__(self):
        self.concurrentReqs = CONCURRENT_REQUESTS
        self.apiTests = []

    def buildTestConfig(self, configFile = 'apitests.json'):
        try:
            with open(configFile, 'r') as cfgfile:
                fullJSON = json.load(cfgfile)
                try:
                    self.apiTests = fullJSON['apitests']
                except KeyError:
                    pass

                try:
                    self.concurrentReqs = fullJSON['concurrentReqs']
                except KeyError:
                    pass

        except FileNotFoundError:
            pass
        return self
        
    def getConcurrentReqs(self):
        return self.concurrentReqs
    
    def getApiTests(self):
        return self.apiTests