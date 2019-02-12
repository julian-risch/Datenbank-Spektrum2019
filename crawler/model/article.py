from scrapy import Item, Field
from scrapy.loader.processors import MapCompose


def remove_newlines(text):
    return text.replace('"', '') \
        .replace('\n', ' ') \
        .replace('\r', '') \
        .strip()


class Article(Item):
    section_url = Field()
    article_url = Field()
    article_title = Field(input_processor=MapCompose(remove_newlines))
    is_commentable = Field()
    timestamp = Field()
