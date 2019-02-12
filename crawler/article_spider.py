from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from crawler.model.article import Article


class ArticleSpider(CrawlSpider):
    name = 'theguardian-articles'
    rules = [
        # Extract links to follow up article pages from article pages
        Rule(LinkExtractor(restrict_xpaths='//div[@class="fc-container__pagination"]/div/div/a[last()]'),
             callback='parse_article_page', follow=True),
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipeline.article_pipeline.FilterDuplicateArticlesPipeline': 0
        }
    }

    def parse_article_page(self, response):
        # Parses article overview page and returns article items
        articles = list()
        selector = Selector(response)
        article_scopes = selector \
            .css('.fc-item') \
            .extract()

        for article_scope in article_scopes:
            article = self.parse_article(article_scope)
            article['section_url'] = response.url
            articles.append(article)

        print(f'Parsed article page: {response.url} and fetched {len(articles)} articles.')
        return articles

    def parse_article(self, article_scope):
        # Extract the data for a single article
        selector = Selector(text=article_scope)
        article_loader = ItemLoader(item=Article(), selector=selector)
        article_loader.default_output_processor = TakeFirst()
        article_loader.add_xpath('article_url', '//div/a/@href')
        article_loader.add_xpath('article_title', '//div/a/text()')
        article_loader.add_xpath('timestamp', '//div/div/aside/time/@datetime')
        article_loader.add_xpath('is_commentable', 'boolean(//div[contains(@class, "fc-item--is-commentable")])')
        return article_loader.load_item()
