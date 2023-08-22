# -*- coding: utf-8 -*-
from .HTTPClient import HTTPClient


class PromptClient(HTTPClient):
    """The main prompt create functions of the billionprompts"""

    def __init__(self, headers=None):
        defaultHeaders = {
            'Content-Type': 'application/json',
        }
        defaultHeaders.update(headers)
        super().__init__(headers=defaultHeaders)

    # prompts for images
    def fcDict(self, text):
        """Description continued
        Examples： text = "a girl in white setting on the grass "
        return: a longer description of the scene.
        Note the output is a stream
        """
        data = {
            "text": text,
        }
        for each in self.post_stream('/api/prompt/fcDict', data):
            yield each

    def descToPrompt(self, text):
        """convert a description  to prompts
        Examples： text = "a girl in white setting on the grass "
        return: a list of prompt word, join it with "," you can get a continuation prompt
        """
        data = {
            "text": text,
        }
        response = self.post('/api/prompt/descToPrompt', data)
        result = [each["en_prompt"] for each in response["data"]]
        return result

    def promptContinu(self, prompt):
        """Supplement and continuation of the input prompt
        Examples： text = "1girl,long hair,white hair"
        return: a list of prompt word, join it with "," you can get a continuation prompt
        """
        data = {
            "text": prompt,
        }
        response = self.post('/api/prompt/promptContinu', data)
        result = [each["en_prompt"] for each in response["data"]]
        return result

    def negativePrompt(self, prompt):
        """Supplement and continuation of the input prompt
        Examples： text = "1girl,long hair,white hair"
        return: a list of prompt word, join it with "," you can get a continuation prompt
        """
        data = {
            "text": prompt,
        }
        response = self.post('/api/prompt/negativePrompt', data)
        result = response["data"]
        return result

    # prompts for language
    def language_task2prompt(self, text):
        """generate a prompt based on the text task
        Note the output is a stream"""
        data = {
            "text": text,
        }
        for each in self.post_stream('/api/chat/task2prompt', data):
            yield each
