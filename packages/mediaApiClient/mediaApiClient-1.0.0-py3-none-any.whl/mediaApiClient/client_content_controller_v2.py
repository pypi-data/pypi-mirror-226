from datetime import date

import requests

from mediaApiClient.content_meta_models import ContentMeta, PageWithElements


class ClientContentControllerV2:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_content_by_id(self, content_id):
        url = f"{self.base_url}/api/v2/contents/{content_id}"
        params = {
            "contentId": content_id
        }

        headers = {
            "Authorization-Client": self.auth_token
        }

        content_response = requests.get(url, params=params, headers=headers)

        if content_response.status_code == 200:
            return ContentMeta(**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")

    def get_content_by_filter(self, filter_request, number=0, size=10):
        payload = filter_request.model_dump_json()
        url = f"{self.base_url}/api/v2/contents"

        params = {
            "number": number,
            "size": size
        }

        headers = {
            "Authorization-Client": self.auth_token,
            "Content-Type": "application/json"
        }

        content_response = requests.post(url, data=payload, headers=headers, params=params)

        if content_response.status_code == 200:
            return PageWithElements[ContentMeta](**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")
