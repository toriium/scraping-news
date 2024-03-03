from enum import Enum, auto


class ArticleError(Enum):
    duplicate_entry = auto()
    not_found = auto()
