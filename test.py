from __future__ import print_function
import time

import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from swagger_client.configuration import Configuration

Configuration().host = "http://localhost:8080/api"

# create an instance of the API class
api_instance = swagger_client.DeploymentsApi()

try:
    # Get deployment details
    api_response = api_instance.get_deployments_collection()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DeploymentsApi->get_deployment: %s\n" % e)
