import requests
import asyncio
import random
import time

import config
import report
from config import TestConfig

jitReportingQ = asyncio.Queue()
offlineReportingQ = asyncio.Queue()
cfg = TestConfig().buildTestConfig()

async def main():
    timestampStart = time.time_ns()
    await runAPITests(cfg)
    timestampFinish = time.time_ns()
    results = []
    
    while not(offlineReportingQ.empty()):
        resp = await offlineReportingQ.get()
        results.append(resp)
    
    duration = round((timestampFinish - timestampStart) / 1000000)
    report.printTestSummary(duration)
    
async def runAPITests(cfg):
    i = 0
    chunkSize = cfg.getConcurrentReqs()
    apiTests = cfg.getApiTests()
    while i < len(apiTests):
        toBeLaunched = len(apiTests) - i if len(apiTests) - i < chunkSize else chunkSize
        tasks = [buildTask(apiTests[j], j) for j in range(i, i + toBeLaunched)]
        i = i + chunkSize
        await asyncio.gather(*tasks)
    await jitReportingQ.put((-1, "STOP"))

def buildTask(testCfg, testIndex):
    match testCfg['method']:
        case 'GET':
            return asyncio.create_task(doGetRequest(testIndex, testCfg['URL'], testCfg['params'], testCfg['headers']))
        case _:
            raise RESTMethodNotImplemented

async def doGetRequest(testIndex, _url, _params, _headers):
    resp = requests.get(url = _url, params = _params, headers=_headers)
    #print(resp.json())
    await putTestResult(resp, testIndex)

async def putTestResult(resp, testIndex):
    await jitReportingQ.put((testIndex, resp))
    await offlineReportingQ.put(resp)

class RESTMethodNotImplemented(Exception):
    pass

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.create_task(report.processTestResults(cfg.getApiTests(), jitReportingQ, loop))
    loop.run_forever()