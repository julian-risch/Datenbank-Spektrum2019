class LogPipeline(object):
    def open_spider(self, spider):
        print(f"Started spider {spider.name}")

    def process_item(self, item, spider):
        print(item)
        return item

    def close_spider(self, spider):
        print(f"Closed spider {spider.name}")
