
import scrapy
import time
from food_spider.utils import load_output

class GenericSpider(scrapy.Spider):

    def __init__(self, redownload=False, continue_scrape=False, infile_previous=None,*args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        if type(redownload) is str:
            redownload=eval(redownload)
        if type(continue_scrape) is str:
            continue_scrape=eval(continue_scrape)

        self.redownload=redownload
        self.continue_scrape=continue_scrape
        self.infile_previous = infile_previous

        # Load previous results, identify failed download, run parse2()
        if self.infile_previous is not None:
            self.products_previous = load_output(self.infile_previous)
            self.products_previous_urls = [x['url'] for x in self.products_previous]


    def parse_failed(self, response, parent_url):
        products_failed = []
        for p in self.products_previous:
            if p['name'] is None:
                # Find all examples
                products_sub = [x for x in self.products_previous if x['item_number'] == p['item_number']]
                if all([x['name'] is None for x in products_sub]):
                    products_failed.append(p)

        self.logger.debug("Number of products to re-try {}".format(len(products_failed)))
        for p in products_failed:
            url = p['url']
            self.logger.debug("URL: {}".format(url))
            time.sleep(1)
            yield scrapy.Request(url=url,
                                 callback=self.parse_detail,
                                 meta=dict(ec_wait=3),
                                 cb_kwargs=dict(parent_url=p['parent_url']))

    def filter_urls(self, urls, s_url, split=False):
        urls = list(set(urls))
        # If we are re-downloading, skip those urls we already have
        if self.continue_scrape:
            # For voila
            if split:
                urls = [x for x in urls if x.split("|")[1] not in self.products_previous_urls]
            else:
                urls = [x for x in urls if x not in self.products_previous_urls]
        self.logger.debug("Num to download: {} for {}".format(len(urls), s_url))
        return urls