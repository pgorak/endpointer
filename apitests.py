import requests
import asyncio
import random
import time

import config
import report
from config import TestConfig

q = asyncio.Queue()

async def main():
    cfg = TestConfig().buildTestConfig()
    timestampStart = time.time_ns()
    await runAPITests(cfg)
    timestampFinish = time.time_ns()
    results = []
    while not(q.empty()):
        resp = await q.get()
        results.append(resp)

    duration = round((timestampFinish - timestampStart) / 1000000)
    report.printTestSummary(cfg.getApiTests(), results, duration)
    
async def runAPITests(cfg):
    i = 0
    chunkSize = cfg.getConcurrentReqs()
    apiTests = cfg.getApiTests()
    while i < len(apiTests):
        toBeLaunched = len(apiTests) - i if len(apiTests) - i < chunkSize else chunkSize
        tasks = [buildTask(apiTests[j]) for j in range(i, i + toBeLaunched)]
        i = i + chunkSize
        await asyncio.gather(*tasks)

def buildTask(testCfg):
    match testCfg['method']:
        case 'GET':
            return asyncio.create_task(doGetRequest(testCfg['URL'], testCfg['params'], testCfg['headers']))
        case _:
            raise RESTMethodNotImplemented

async def doGetRequest(_url, _params, _headers):
    resp = requests.get(url = _url, params = _params, headers=_headers)
    #print(resp.json())
    await q.put(resp)

class RESTMethodNotImplemented(Exception):
    pass

if __name__ == '__main__': 
    asyncio.run(main())