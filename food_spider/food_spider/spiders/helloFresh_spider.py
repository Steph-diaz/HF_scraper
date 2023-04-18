from pathlib import Path
import scrapy
import requests
from scrapy import signals, Selector

from food_spider.cdriver import CDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
from scrapy.shell import inspect_response
from food_spider.spiders.generic_spider import GenericSpider
from food_spider.items import FoodSpiderItem

class HelloFreshSpider(GenericSpider):
    name = "helloFresh"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(HelloFreshSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        CDriver().driver.quit()

    def start_requests(self):
        start_url = 'https://www.hellofresh.ca/menus?locale=en-CA'

        urls = []
        CDriver().driver.delete_all_cookies()
        CDriver().driver.get(start_url)
        print(start_url)
        input("Scroll page down and wait for pop-up, Press Enter to continue...")
        # go into each menu item (open modal) and get the detail information href of each
        x = CDriver().driver.find_elements(By.CSS_SELECTOR,
                                           'div[data-test-id="recipe-card-component"]')
        print(len(x))
        input("Scroll page down and wait for pop-up, Press Enter to continue...")
        for my_elem in x:
            # urls.append(my_elem.get_attribute("href"))

            # click on recipe
            my_elem.click()
            # get link of recipe details
            link = WebDriverWait(CDriver().driver, 5).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".web-i2y57x")))
            link2 = WebDriverWait(CDriver().driver, 5).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".ReactModal__Content--after-open")))
            h2text = link2.find_element(By.CSS_SELECTOR, '.web-q5jmhc')
            urltext = h2text.get_attribute("href")
            urls.append(urltext)
            print(urltext)
            # go back
            time.sleep(3)
            link.click()

        urls = list(set(urls))
        print(urls)
        # input("Scroll page down and wait for pop-up, Press Enter to continue...")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta=dict(ec_scroll_to_end=True, ec_wait=1))

    def parse(self, response):

        product_link = response.url
        firstname = response.css('h1.sc-f1f602c0-0::text').get()
        secondname = response.css('h4.sc-f1f602c0-0::text').get(default='')
        pdf_link = response.css('a[href*=pdf]::attr(href)').get(default='')
        # # Save pdf
        # pdf_data = requests.get(pdf_link)
        # # outdir = Path(spider.settings['FILES_STORE'])
        # filename = firstname + '.pdf'
        # print(f'Saving {filename}')
        # with open(filename, 'wb') as file:
        #     file.write(pdf_data.content)


        allergens_list = response.xpath('//div[@data-test-id="recipe-description-allergen"]/span[@class="sc-f1f602c0-0 XJyHj"]/text()').getall()
        utensils_list = response.xpath('//div[@data-test-id="utensils-list-item"]/span[2]/text()').getall()
        # Some Ingredients contain these
        ingred_contain_list = response.xpath('//div[@class="sc-f1f602c0-0 ifxZyI"]/p/span[2]/text()').getall()

        # Making Dict of nutrient and values
        nut_list = response.xpath('//span[@class="sc-f1f602c0-0 evLAvX"]/text()').getall()
        nut_values_raw = response.xpath('//div[@data-test-id="nutrition-step"]/span[@class="sc-f1f602c0-0 gLLWSr"]//text()').getall()
        nut_values_list = [nut_values_raw[i] + nut_values_raw[i+2] for i in range(0,len(nut_values_raw),3)]
        nutrition = dict(zip(nut_list, nut_values_list))
        # Making Dict of ingredients
        ingred_list = response.xpath('//div[@class="sc-f1f602c0-0 ifxZyI"]/p[2]/text()').getall()
        ingred_values_list = response.xpath('//div[@class="sc-f1f602c0-0 ifxZyI"]/p[1]/text()').getall()
        ingredients = dict(zip(ingred_list, ingred_values_list))

        # Making dict of instructions
        step_number = response.xpath('//div[@class="sc-f1f602c0-0 jBFkrx"]/span/text()').getall()
        step_descrip =response.xpath('//div[@class="sc-f1f602c0-0 kOYOQw"]/span/p/text()').getall()
        step_numb_formatted = [f'Instruction {x[0:]}' for x in step_number]
        instructions = dict(zip(step_numb_formatted, step_descrip))

        product = {
            'name': firstname + " " + secondname,
            'product_pdf_link': pdf_link,
            'product_link': product_link,
            'description': response.xpath('//span[@class="sc-f1f602c0-0 XJyHj"]/p/text()').get(
                default=''),
            'preparation_time': response.xpath('//span[@class="sc-f1f602c0-0 gLLWSr"]/text('
                                               ')').get(default=''),
            'difficulty': response.xpath('//span['
                                         '@data-translation-id="recipe-detail.level-number-2"]/text()').get(default=''),
            'tags': response.xpath('//div[@data-test-id="recipe-description-tag"]/span[@class="sc-f1f602c0-0 XJyHj"]/text()').get(default=''),
            'allergens': ", ".join(allergens_list),
            'allergens_disclaimer': response.xpath('//span[@data-translation-id="recipe-detail.allergens-disclaimer"]/text()').get(),
            'nutritional_info': response.xpath('//span['
                                            '@data-translation-id="recipe-detail.recipe-detail.per-serving"]/text()').get(),
            'nutrition': nutrition,
            'ingredients': ingredients,
            'utensils': ", ".join(utensils_list),
            'ingredients_contain': ", ".join(list(set(list((", ".join(ingred_contain_list)).split(", "))))),
            'instructions': instructions,
            # 'file_urls': [pdf_link],
        }

        yield product

        if pdf_link:
            item = FoodSpiderItem()
            # pdf_url = eval(pdf_link)
            item['file_urls'] = [pdf_link]
            yield item
