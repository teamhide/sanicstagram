from dataclasses import dataclass


@dataclass
class ArticleDto:
    pw: str = None
    subject: str = None
    content: str = None
