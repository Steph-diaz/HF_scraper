# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from io import BytesIO
import requests
from PIL import Image
from pathlib import Path


class FoodSpiderPipeline:
    def process_item(self, item, spider):
        return item


class PostScrapeImageDownloader:
    def process_item(self, item, spider):
        for image_url in item['image_urls']:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            outdir = Path(spider.settings['IMAGES_STORE'])
            img.save(Path(outdir) / Path(image_url).name)
        return item