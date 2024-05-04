from fastapi.testclient import TestClient
from httpx import Response

from app.app import app


def evaluation_provider_function(response: Response):
    print("Endpoint response: {response}".format(response=response))

    def evaluate_function(expected_code: int, **kwargs):
        assert response.status_code == expected_code
        result_dict = response.json()
        for key, value in kwargs.items():
            assert value == result_dict[key]

    return evaluate_function


class TestEndpointExecutor:

    __test__ = False

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = TestClient(app)

    def do_get_endpoint(self, params: str | None):

        endpoint_with_params = self.endpoint
        if params != None:
            endpoint_with_params = endpoint_with_params + "?" + params

        result = self.client.get(self.endpoint)

        return evaluation_provider_function(result)

    def do_post_endpoint(self, body: dict):
        result = self.client.post(self.endpoint, json=body)
        return evaluation_provider_function(result)
