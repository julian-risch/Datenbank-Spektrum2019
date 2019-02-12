from scrapy import Item, Field
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


def remove_quotes_and_newlines(text):
    # Todo: Optimize removing these chars: ", \n, \r
    return text.replace('"', '') \
        .replace('\n', ' ') \
        .replace('\r', '') \
        .replace('<blockquote>', '[') \
        .replace('</blockquote>', ']') \
        .strip()


def remove_comment_id_prefix(text):
    return str(text) \
        .replace('comment-', '') \
        .replace('#', '')


def convert_to_int(text):
    return int(text)


def extract_comment_id(text):
    id_text = remove_comment_id_prefix(text)
    return convert_to_int(id_text)


def extract_comment_text(html):
    text = remove_tags(html, keep=('blockquote',))
    return remove_quotes_and_newlines(text)


class Comment(Item):
    comment_id = Field(input_processor=MapCompose(extract_comment_id))
    comment_author = Field(input_processor=MapCompose(remove_quotes_and_newlines))
    comment_text = Field(input_processor=MapCompose(extract_comment_text))
    timestamp = Field()
    article_url = Field()
    comment_url = Field()
    parent_comment_id = Field(input_processor=MapCompose(remove_comment_id_prefix))
    upvotes = Field(input_processor=MapCompose(convert_to_int))
