from numpy import array
from requests import post
from dataclasses import dataclass
from typing import Optional, List
from maz import compose

@dataclass
class Result:

    data:   Optional[list]  = None
    error:  Optional[str]   = None

@dataclass
class EmbeddingSDK:
    
    url: str

    def __call__(self, text_list: List[List[str]], dims: int = 100) -> Result:

        """
            Converts a list of sentences, or list of list of strings, into a list of embeddings.
            Each list of strings will be converted into a single embedding.

            :param text_list: A list of sentences, or list of list of strings, to be converted into embeddings.
            :param dims: The number of dimensions of the embedding. Must be 3, 5 or 100.
            :return: A list of embeddings, or a list of list of embeddings, depending on the input.
        """

        try:
            response = post(
                self.url, 
                json={
                    "query": """
                        query TextQuery($sentences: [[String!]!]!) {
                            textCollection(corpuses: $sentences, model: D"""+str(dims)+""")
                        }
                    """,
                    "variables": {
                        "sentences": text_list,
                    }
                }
            )

            if response.status_code == 200:
                if "errors" in response.json():
                    return Result(error=response.json()["errors"][0]["message"])
                return Result(
                    data=array(
                        response.json()["data"]["textCollection"]
                    )
                )

        except Exception as e:
            return Result(error=str(e))

from pickle import loads
from gzip import decompress
from base64 import b64decode

@dataclass
class EmbeddingSDKCompressed:
    
    url: str

    def __call__(self, text_list: List[List[str]], dims: int = 100) -> Result:

        """
            Converts a list of sentences, or list of list of strings, into a list of embeddings.
            Each list of strings will be converted into a single embedding.

            :param text_list: A list of sentences, or list of list of strings, to be converted into embeddings.
            :param dims: The number of dimensions of the embedding. Must be 3, 5 or 100.
            :return: A list of embeddings, or a list of list of embeddings, depending on the input.
        """

        try:
            response = post(
                self.url, 
                json={
                    "query": """
                        query TextQuery($sentences: [[String!]!]!) {
                            textCollectionCompressed(corpuses: $sentences, model: D"""+str(dims)+""")
                        }
                    """,
                    "variables": {
                        "sentences": text_list,
                    }
                }
            )

            if response.status_code == 200:
                if "errors" in response.json():
                    return Result(error=response.json()["errors"][0]["message"])
                return Result(
                    data=list(
                        list(
                            map(
                                compose(
                                    array,
                                    loads,
                                ),
                                loads(
                                    decompress(
                                        b64decode(
                                            response.json()["data"]["textCollectionCompressed"].encode()
                                        )
                                    )
                                )
                            )
                        )
                    )
                )

        except Exception as e:
            return Result(error=str(e))