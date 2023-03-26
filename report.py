from termcolor import colored 

import verify

def printTestSummary(apiTests, results, duration):
    results = [list(z) for z in zip(apiTests, results)]
    howManyFailed = 0
    for row in results:
        testResult = verify.verify(row[0], row[1])
        if not testResult['status']:
            howManyFailed += 1
            errorCode = colored(testResult['resultMessage'], 'red')
            print(row[0], errorCode)
    print('===============================================================')
    print('Executed ', len(results), ' API tests in ', duration, ' milliseconds.')
    print('===============================================================')
    if howManyFailed > 0 :
        failedMessage = colored(str(howManyFailed) + ' test(s) failed.', 'red')
        print(failedMessage)