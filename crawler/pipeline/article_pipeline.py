from scrapy.exceptions import DropItem

from crawler.utils import hash_article


class FilterDuplicateArticlesPipeline(object):
    def __init__(self):
        # hashing decreases the memory consumption while keeping the collision probability virtually zero
        self.article_url_hashes = set()

    def process_item(self, item, spider):
        article_url_hash = hash_article(item)
        if article_url_hash in self.article_url_hashes:
            print(f'Filter deleted duplicate article "{item["article_title"]}" with url: {item["article_url"]}')
            raise DropItem()
        else:
            self.article_url_hashes.add(article_url_hash)
            return item
