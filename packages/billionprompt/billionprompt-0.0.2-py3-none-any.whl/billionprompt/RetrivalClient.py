# -*- coding: utf-8 -*-
from .HTTPClient import HTTPClient
from .utils import is_url


class RetrivalClient(HTTPClient):
    """The main data retrival functions of the billionprompts"""

    def __init__(self, headers=None):
        defaultHeaders = {
            'Content-Type': 'application/json',
        }
        defaultHeaders.update(headers)
        super().__init__(headers=defaultHeaders)
        self.image_url_base = "https://d22zc55in2n9wy.cloudfront.net/"

    # retrival images
    def image2image(self, imageurl):
        """ retrival similarity images based on the input imageurl
        :param imageurl: a url of an image
        :return: a list of image url
        """
        if not is_url(imageurl):
            raise Exception("The input should be an image url ")

        data = {
            "img_str": imageurl,
            "input_type": "image",
            "count": 10,
        }
        response = self.post('/api/retrieval', data)
        result = [self.image_url_base + each["image_name"] for each in response["data"]["img_name"]]
        return result

    def text2image(self, text):
        """ retrival similarity images based on the input texts
        :param text: a description or a prompt of an image
        :return: a list of image url
        """
        data = {
            "img_str": text,
            "input_type": "text",
            "count": 10,
        }
        response = self.post('/api/retrieval', data)
        result = [self.image_url_base + each["image_name"] for each in response["data"]["img_name"]]
        return result

    # retrival aduio
    def text2audio(self, prompt):
        """ retrival similarity audios based on the input texts
        :param prompt: a description or a prompt of an audio
        :return:
        """
        pass

    # retrival language prompt
    def language_prompt_retrival(self, prompt):
        """ retrival similarity audios based on the input texts
        :param prompt: a description or a prompt of a language task
        :return:
        """
        data = {
            "text": prompt,
        }
        response = self.post('/api/languagePrompt/search', data)
        result = [each["prompt"] for each in response["data"]]
        return result
