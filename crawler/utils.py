import contextlib
import csv
import hashlib
import os


def remove_file_if_exists(file):
    with contextlib.suppress(FileNotFoundError):
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, file)
        os.remove(path)


def save_json_to_csv(filename, json):
    with open(filename, "w+") as file:
        writer = csv.DictWriter(file, json[0].keys(), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in json:
            writer.writerow(row)


def load_article_urls(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        urls = []
        next(reader, None)
        for article in reader:
            urls.append(article[6])
        return urls


def hash_article(article):
    url = article['article_url']
    return hashlib.md5(bytes(url, 'utf8')).digest()
