from scrapy.exceptions import DropItem


class FilterDeletedCommentsPipeline(object):
    def process_item(self, item, spider):
        if item['comment_text']:
            return item
        else:
            print(f'Filter deleted comment by {item["comment_author"]} with id: {item["comment_id"]} ')
            raise DropItem()
