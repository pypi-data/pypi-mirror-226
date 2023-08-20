import json
import pprint

import requests as requests
from django.contrib.auth import get_user_model

from app_generic_api.standard_utils import RequestMethodType
from app_generic_api.views import GenericApiView
User = get_user_model()
# serializer_data = {
#         "api_slug": "list_related_families",
#         "body": {},
#         "query_params": {}
#     }

# serializer_data = {
#         "api_slug": "retrieve_given_family",
#         "body": {},
#         "query_params": {
#             "object_id": "a63917d8-0755-48f2-8428-c6858ec71c32"
#         }
#     }

# serializer_data = {
#         "api_slug": "retrieve_given_person",
#         "body": {},
#         "query_params": {
#             "object_id": "a63917d8-0755-48f2-8428-c6858ec71c32"
#         }
#     }


def test():
    class FakeRequest:
        def __init__(self):
            self.user = User.objects.filter(profile__isnull=False).first()

    serializer_data = {
            "api_slug": "list_related_families",
            "body": {},
            "query_params": {}
        }
    method = "GET"
    response = GenericApiView().generic_api_call(
        serializer_data=serializer_data,
        method=method,
        request=FakeRequest()
    )
    # return response.data
    return json.loads(json.dumps(response.data))

def test_api_slug(api_slug, body, query_params, method, base_url="https://0.0.0.0:8000/"):
    #TODO created by? metadata of component type?
    serializer_data = {
        "api_slug": api_slug,
        "body": body,
        "query_params": query_params
    }
    # method = RequestMethodType.DELETE

    ##########################################################
    request_data = {
        "api_slug": serializer_data["api_slug"],
    }
    if len(serializer_data["query_params"].keys()):
        request_data["query_params"] = json.dumps(serializer_data["query_params"])
    if len(serializer_data["body"].keys()):
        request_data["body"] = json.dumps(serializer_data["body"])
    print("req data = ",request_data)
    generic_api_url = base_url + "api/generic_api/"
    if method == RequestMethodType.GET:
        response = requests.get(
            url=generic_api_url,
            params=request_data,
            verify=False,
        )
    else:
        if method == RequestMethodType.POST:
            request_method = requests.post
        elif method == RequestMethodType.PUT:
            request_method = requests.put
        elif method == RequestMethodType.PATCH:
            request_method = requests.patch
        elif method == RequestMethodType.DELETE:
            request_method = requests.delete
        else:
            raise Exception(f"Invalid method: {method}")
        response = request_method(
            url=generic_api_url,
            data=request_data,
            verify=False,
        )
    print(response.status_code)
    if (response.status_code in [200, 400, 201]):
        try:
            pprint.pprint(response.json())
        except:
            print("error while printing response json")

    # print(response.text)
    # print(response.raw)
    # return response.json()
    return response
