# vim:fenc=utf-8
#
# Copyright (C) 2023 dbpunk.com Author imotai <codego.me@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" """
import asyncio
import json
import aiohttp
import logging
import requests

logger = logging.getLogger(__name__)


class CodellamaClient:

    def __init__(self, endpoint, key, prefix, ai_name, user_name, grammar):
        self.api = endpoint + "/completion"
        self.ai_name = ai_name
        self.user_name = user_name
        self.grammar = grammar
        self.prefix = prefix

    def prompt(self, user_input, temperature=0.2, chat_history=""):
        prompt = f"""{self.prefix}
{chat_history}
{self.user_name}: {user_input}
{self.ai_name}:"""
        logging.info(f"{prompt}")
        data = {
            "n_predict": 1024,
            "grammar": self.grammar,
            "prompt": prompt,
            "temperature": temperature,
            "repeat_last_n": 256,
            "top_p": 0.95,
            "stop": [
                "</s>",
                "\n",
                "%s:" % self.ai_name,
                "%s:" % self.user_name,
            ],
        }
        response = requests.post(self.api, data=json.dumps(data))
        return response.json()
