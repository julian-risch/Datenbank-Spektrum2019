from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from crawler.model.comment import Comment


class CommentSpider(CrawlSpider):
    name = 'theguardian-comments'
    rules = [
        # Extract links to the comment page from article pages
        Rule(LinkExtractor(restrict_xpaths='//*[@id="comments"]/div/div/div[1]/div/div/h2/a'),
             callback='parse_comment_page', follow=True),
        # Extract links to follow up comment pages from article pages
        Rule(LinkExtractor(restrict_xpaths='//*[@id="top"]/div[5]/div/div/div[2]/div[1]/div/div/a[last()]'),
             callback='parse_comment_page', follow=True),
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipeline.comment_pipeline.FilterDeletedCommentsPipeline': 0
        }
    }

    def parse_comment_page(self, response):
        # Parses comment pages and returns comment data
        comments = list()
        selector = Selector(response)
        comment_scopes = selector.css('.d-comment').extract()
        article_url = selector.xpath('//h1[@class="content__headline"]/a/@href').extract_first()

        for comment_scope in comment_scopes:
            comment = self.parse_comment(comment_scope)
            comment.setdefault('comment_text', None)
            comment['article_url'] = article_url
            comment['comment_url'] = response.url
            comments.append(comment)

        print(f'Parsed page: {response.url} and fetched {len(comments)} comments.')
        return comments

    def parse_comment(self, comment_scope):
        # Extract the data for a single comment
        selector = Selector(text=comment_scope)
        comment_loader = ItemLoader(item=Comment(), selector=selector)
        comment_loader.default_output_processor = TakeFirst()
        comment_loader.add_xpath('comment_id', '//li/@id')
        comment_loader.add_xpath('comment_author', '//div/div[1]/div/span[1]/a/span/text()')
        comment_loader.add_xpath('comment_text', '//div/div[2]/div[2]/div[@class="d-comment__body"]')
        comment_loader.add_xpath('timestamp', '//div/div[1]/div/div/a/time/@datetime')
        comment_loader.add_xpath('parent_comment_id', '//a[@class="js-discussion-author-link"]/@href')
        comment_loader.add_xpath('upvotes', '//div/div[2]/div[1]/span/span[1]/text()')
        return comment_loader.load_item()
