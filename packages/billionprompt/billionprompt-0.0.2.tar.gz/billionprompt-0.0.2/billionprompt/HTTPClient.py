# -*- coding: utf-8 -*-
import requests


class HTTPClient:
    def __init__(self, headers=None):
        self.baseUrl = 'https://api.billionprompt.com'
        self.headers = headers if headers else {}

    def get(self, url):
        response = requests.get(self.baseUrl + url, headers=self.headers)
        responseData = response.json()
        return responseData

    def post(self, url, data):
        response = requests.post(self.baseUrl + url, params=data, headers=self.headers)
        responseData = response.json()
        if "error" in responseData:
            raise Exception(responseData["error"])
        return responseData

    def post_stream(self, url, data):
        response = requests.post(self.baseUrl + url, params=data, headers=self.headers, stream=True)
        if response.status_code == 200:
            for data_chunk in response.iter_content(chunk_size=1024):
                # 处理接收到的数据块
                yield data_chunk.decode("utf-8")
        else:
            raise Exception(response.status_code)
