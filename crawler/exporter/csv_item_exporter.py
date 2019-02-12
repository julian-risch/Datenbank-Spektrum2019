import csv

from scrapy.exporters import CsvItemExporter


class CsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = ','
        kwargs['quoting'] = csv.QUOTE_NONNUMERIC
        super(CsvItemExporter, self).__init__(*args, **kwargs)
