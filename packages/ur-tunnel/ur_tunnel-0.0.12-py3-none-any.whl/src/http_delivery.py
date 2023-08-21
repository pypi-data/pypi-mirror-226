from typing import TypedDict

class LocalRequest(TypedDict, total=False):
    id: str
    path: str
    query: str
    method: str
    headers: dict
    body: str

class LocalResponse(TypedDict, total=False):
    request_id: str
    headers: dict
    content: str
    status_code: int
