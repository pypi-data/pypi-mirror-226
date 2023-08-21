"""Chat Completions Schemas"""
from typing import Dict, List, Literal

from aiofauna import Document, Field

Role = Literal["assistant", "user", "system", "function"]
Model = Literal["gpt-4-0613", "gpt-3.5-turbo-16k-0613"]
Size = Literal["256x256", "512x512", "1024x1024"]
Format = Literal["url", "base64"]

from typing import Dict, List, Literal, Union

from aiofauna import *
from aiofauna.typedefs import *

Vector = List[float]
Value = str | int | float | bool | List[str]
MetaData = Dict[str, Value]
Filter = Literal["$eq", "$ne", "$lt", "$lte", "$gt", "$gte", "$in", "$nin"]
AndOr = Literal["$and", "$or"]
Query = Union[
    Dict[str, Union[Value, "Query", List[Value], List["Query"]]],
    Dict[AndOr, List[Dict[str, Union[Value, "Query", List[Value], List["Query"]]]]],
]
Size = Literal["256x256", "512x512", "1024x1024"]
Format = Literal["url", "b64_json"]
