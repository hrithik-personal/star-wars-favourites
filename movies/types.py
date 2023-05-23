from typing import TypedDict


class MovieTypedDict(TypedDict):
    title: str
    release_date: str
    created: str
    updated: str
    url: str
    is_favourite: bool
