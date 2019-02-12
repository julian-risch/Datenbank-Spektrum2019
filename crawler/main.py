import os
import sys
from argparse import ArgumentParser
from csv import DictReader
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

from crawler.model.article import Article
from crawler.article_spider import ArticleSpider
from crawler.comments_spider import CommentSpider
from crawler.section_loader import get_sections
from crawler.utils import remove_file_if_exists
from crawler.fingerprints_calculator import calculate_fingerprint


def get_crawler_settings(output_file):
    return {
        'FEED_URI': output_file,
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': 'ERROR',
        'FEED_FORMAT': output_format,
        'FEED_EXPORTERS': {
            'csv': 'crawler.exporter.csv_item_exporter.CsvItemExporter'
        }
    }


def load_articles(input_file):
    with open(input_file, 'r', newline='') as f:
        reader = DictReader(f)
        if set(reader.fieldnames) != set(Article.fields):
            exit('Invalid input file')

        for row in reader:
            row['is_commentable'] = (row['is_commentable'] == '1')
            article = Article(row)
            yield article


@defer.inlineCallbacks
def crawl_section_articles(sections, output_file):
    # Run a spider for every section in sequence in the same process
    runner = CrawlerRunner(get_crawler_settings(output_file=output_file))

    for section in sections:
        print(f'\nLoading articles for section \'{section["title"]}\'.')
        section_url = section['url'] + '/all'
        yield runner.crawl(ArticleSpider, start_urls=[section_url])

    reactor.stop()


@defer.inlineCallbacks
def crawl_article_comments(articles, output_file):
    # Run a spider for every article in sequence in the same process
    runner = CrawlerRunner(get_crawler_settings(output_file=output_file))

    for article in articles:
        print(f'\nLoading comments for article \'{article["article_title"]}\'')
        article_url = article['article_url']
        yield runner.crawl(CommentSpider, start_urls=[article_url])

    reactor.stop()


def crawl_all_articles(output_file):
    print('Loading sections...')
    sections = get_sections()
    print(f'Fetched {len(sections)} sections.')

    print('Loading articles for sections...')
    remove_file_if_exists(output_file)

    crawl_section_articles(sections, output_file)
    reactor.run()


def crawl_all_comments(input_file, output_file):
    print('Crawling comments...')
    articles = load_articles(input_file)
    commentable_articles = (article for article in articles if article['is_commentable'])
    remove_file_if_exists(output_file)

    crawl_article_comments(commentable_articles, output_file)
    reactor.run()


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
output_format = 'csv'
output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
default_file_articles = os.path.join(output_dir, f'articles.{output_format}')
default_file_comments = os.path.join(output_dir, f'comments.{output_format}')
default_file_fingerprints = os.path.join(output_dir, f'fingerprints.{output_format}')

if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    comment_parser = subparsers.add_parser('comments')
    comment_parser.add_argument('-i', dest='input', default=default_file_articles)
    comment_parser.add_argument('-o', dest='output', default=default_file_comments)

    article_parser = subparsers.add_parser('articles')
    article_parser.add_argument('-o', dest='output', default=default_file_articles)

    fingerprint_parser = subparsers.add_parser('fingerprints')
    fingerprint_parser.add_argument('-i', dest='input', default=default_file_comments)
    fingerprint_parser.add_argument('-o', dest='output', default=default_file_fingerprints)

    args = vars(parser.parse_args())
    if args['command'] == 'articles':
        if not os.path.isdir(os.path.dirname(args['output'])):
            exit('Invalid output path.')
        else:
            crawl_all_articles(args['output'])
    elif args['command'] == 'comments':
        if not os.path.isdir(os.path.dirname(args['output'])):
            exit('Invalid output path.')
        elif not os.path.isfile(args['input']):
            exit('Invalid input path.')
        else:
            crawl_all_comments(args['input'], args['output'])
    elif args['command'] == 'fingerprints':
        if not os.path.isdir(os.path.dirname(args['output'])):
            exit('Invalid output path.')
        elif not os.path.isfile(args['input']):
            exit('Invalid input path.')
        else:
            calculate_fingerprint(args['input'], args['output'])
    else:
        parser.print_help()
        exit(2)
