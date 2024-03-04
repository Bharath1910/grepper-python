"""
The MIT License

Copyright (c) 2010-2023 Grepper, Inc. (https://www.grepper.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import annotations

from typing import Optional, List

from .answer import GrepperAnswer
from .exceptions import BadRequest
from .exceptions import Unauthorized
from .exceptions import Forbidden
from .exceptions import NotFound
from .exceptions import MethodNotAllowed
from .exceptions import TooManyRequests
from .exceptions import InternalServerError
from .exceptions import ServiceUnavailable

import requests


def exception_handler(status_code):
    if status_code == 400:
        return BadRequest
    elif status_code == 401:
        return Unauthorized
    elif status_code == 403:
        return Forbidden
    elif status_code == 404:
        return NotFound
    elif status_code == 405:
        return MethodNotAllowed
    elif status_code == 429:
        return TooManyRequests
    elif status_code == 500:
        return InternalServerError
    elif status_code == 503:
        return ServiceUnavailable


class Grepper:
    """
    Python Grepper API Wrapper
    """
    def __init__(self, api_key: str):
        self._api_key = api_key

    def search(
        self, query: str = False, similarity: Optional[int] = 60
    ) -> List[GrepperAnswer]:
        """This function searches all answers based on a query.

        Args:
            query (str, optional): Query to search through answer titles. ex: "Javascript loop array backwords". Defaults to False.
            similarity (Optional[int], optional): How similar the query has to be to the answer title. 1-100 where 1 is really loose matching and 100 is really strict/tight match. Defaults to 60.

        Returns:
            GrepperAnswer
        """
        response = requests.get(
            "https://api.grepper.com/v1/answers/search",
            params={"query": query, "similarity": similarity},
            auth=(self._api_key, ""),
        )
        if response.status_code != 200:
            raise exception_handler(response.status_code)
        json_response = response.json()
        data = []
        for answer in json_response["data"]:
            new_answer = GrepperAnswer(
                id=answer["id"],
                content=answer["content"],
                author_name=answer["author_name"],
                author_profile_url=answer["author_profile_url"],
                title=answer["title"],
                upvotes=answer["upvotes"],
                downvotes=answer["downvotes"],
            )
            data.append(new_answer)
        return data
    
    def fetch_answer(
        self, id: int
    ) -> GrepperAnswer:
        """This function returns an answer specified by the id.

        Args:
            id (int, required): The id for the specified answer. ex: "560676 ".

        Returns:
            GrepperAnswer
        """
        response = requests.get(
            f"https://api.grepper.com/v1/answers/{id}",
            auth=(self._api_key, "")
        )
        if response.status_code != 200:
            raise exception_handler(response.status_code)
        json_response = response.json()
        answer = GrepperAnswer(
            id=json_response["id"],
            content=json_response["content"],
            author_name=json_response["author_name"],
            author_profile_url=json_response["author_profile_url"],
            title=json_response["title"],
            upvotes=json_response["upvotes"],
            downvotes=json_response["downvotes"],
        )
        return answer
    
    def update_answer(
        self, id: int, answer: str
    ):
        """This function returns an answer specified by the id.

        Args:
            id (int, required): The id for the specified answer. ex: "560676 ".
            answer (str, required): The answer you want it to update to. ex "new answer content here".

        Returns:
            Dict
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = f"""answer[content]={answer}"""
        response = requests.post(
            f"https://api.grepper.com/v1/answers/{id}",
            headers=headers,
            data=data,
            auth=(self._api_key, "")
        )
        if response.status_code != 200:
            raise exception_handler(response.status_code)
        else:
            return response.json()