from dataclasses import dataclass


@dataclass
class ArticleEntity:
    id: int = None
    pw: str = None
    subject: str = None
    content: str = None
