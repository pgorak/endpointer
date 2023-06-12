# endpointer
Simple, asynchronous API tests.

endpointer is a very lightweight tool for REST API testing written in Python. It's goal is to take full advantage of Python asyncio library to perform multiple API requests at the same time, shortening the overal test execution time. endpointer is meant to be used by developers, to test the internal APIs.

Features:
- GET requests
- checking of response codes
- checking of response body
- simple reporting

To be added:
- other REST verbs

Usage:
$python apitests.py

The apitests.json file contains a sample test configuration.

Pull requests are welcome.
