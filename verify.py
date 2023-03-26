def verify(testConfig, response):
    match testConfig['method']:
        case 'GET':
            return verifyGET(testConfig, response)
        case _:
            pass

def verifyGET(testConfig, response):
    if response.status_code >= 400:
        return {'status': False, 'resultMessage': response.status_code}
    elif response.status_code >= 200 and response.status_code < 400:
        try:
            if response.json() == testConfig['expectedResult']:
                return {'status': True, 'resultMessage': ''}
            else:
                return {'status': False, 'resultMessage': 'Expected value did not match. Actual value: ' +
                                                 response.text}
        except KeyError:
            return {'status': True, 'resultMessage': ''}
    else:
        return {'status': True, 'resultMessage': ''}