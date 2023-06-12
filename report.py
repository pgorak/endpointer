from termcolor import colored 

import csv
from datetime import datetime
import verify

resultsCsv = []

def printTestSummary(duration):
    howManyFailed = 0
    for row in resultsCsv:
        if row[1] != 'PASS':
            howManyFailed += 1
    print('===============================================================')
    print('Executed ', len(resultsCsv), ' API tests in ', duration, ' milliseconds.')
    print('===============================================================')
    if howManyFailed > 0 :
        failedMessage = colored(str(howManyFailed) + ' test(s) failed.', 'red')
        print(failedMessage)
    writeResultsToFile()

async def processTestResults(apiTests, queue, loop):
    while True:
        resultTuple = await queue.get()
        testIndex, result = resultTuple
        if result == "STOP":
            break
        testResult = verify.verify(apiTests[testIndex], result)
        if not testResult['status']:
            errorCode = colored(testResult['resultMessage'], 'red')
            print(apiTests[testIndex], errorCode)
            resultsCsv.append([apiTests[testIndex], testResult['resultMessage']])
        else:
            passMsg = colored('PASS', 'green')
            print(apiTests[testIndex], passMsg)
            resultsCsv.append([apiTests[testIndex], 'PASS'])
        print('')

    loop.stop()

def writeResultsToFile():
    fileName = 'report-' + datetime.isoformat(datetime.now()).replace(':', '.') + '.csv'
    with open(fileName, 'w', newline = '') as reportFile:
            csvWriter = csv.writer(reportFile, delimiter=',')
            for result in resultsCsv:
                csvWriter.writerow(result)
