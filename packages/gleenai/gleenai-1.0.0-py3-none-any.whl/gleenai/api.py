import requests
import json

class GleenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def set_api_key(self, key):
        self.api_key = key

    def send_message(self, query_text, thread_id=None, stream=False, functions=[], id=None, **kwargs):
        if not self.api_key:
            raise ValueError("Please set the API key first.")

        url = 'https://api.gleen.ai/api/v1/send_message'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            "query_text": query_text,
            "thread_id": thread_id,
            "stream": stream,
            "locale": "en",
            "functions": functions
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

