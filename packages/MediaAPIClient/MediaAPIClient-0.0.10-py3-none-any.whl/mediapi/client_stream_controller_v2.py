import requests

from stream_models import StreamUrl


class ClientStreamControllerV2:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_stream_for_content(self, content_id, manifest, use_https, account_id):
        url = f"{self.base_url}/api/v2/stream/contents/{content_id}"
        params = {
            "manifest": manifest,
            "useHttps": str(use_https).lower(),
            "accountId": account_id
        }
        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return StreamUrl(**response.json())
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")
