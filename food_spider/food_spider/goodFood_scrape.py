from pathlib import Path
from cdriver import CDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
import urllib.request
import json


url = 'https://www.makegoodfood.ca/recipes'

urls = []

CDriver().driver.delete_all_cookies()
CDriver().driver.get(url)
print(url)
input("Scroll page down and wait for pop-up, Press Enter to continue...")

# Get the sections


sections = CDriver().driver.find_elements(By.XPATH, "//div[@id='selected-recipes']/div["
                                                    "@class='mt-5']/section/div[@class='relative grid mt-6 z-0 grid-cols-1 gap-x-6 gap-y-10 md:grid-cols-3']/a")

# ### For testing #####
# sections = CDriver().driver.find_elements(By.XPATH, "//div[@id='selected-recipes']/div["
#                                                   "@class='mt-5'][1]/section/div[@class='relative grid mt-6 z-0 grid-cols-1 gap-x-6 gap-y-10 md:grid-cols-3']/a[1]")

##########################
print(len(sections))
input("Scroll page down and wait for pop-up, Press Enter to continue...")
for my_elem in sections:

    urltext = my_elem.get_attribute("href")
    urls.append(urltext)
    print(urltext)
    # go back
    time.sleep(1)


urls = list(set(urls))
# urls_1 = urls[0:1]

print(urls)
product = []

for url in urls:

    values_tp = []
    values_list = []
    CDriver().driver.get(url)
    page = WebDriverWait(CDriver().driver, 7).until(EC.visibility_of_element_located((
        By.XPATH, "//section[@data-testid='product-detail-page-main']")))

    name = page.find_element(By.XPATH, '//h1[@data-testid="title"]').text
    name2 = page.find_element(By.XPATH, '//h2[@data-testid="text"]').text
    page_url = url

    try:
        cook_time = page.find_element(By.XPATH, '//div[@class="flex py-3 border-gray-300 '
                                                'border-r-2 last:border-0 pl-5"]/p').text
    except NoSuchElementException:
        cook_time = ''

    try:
        energy = page.find_element(By.XPATH, '//div[@class="flex py-3 border-gray-300 border-r-2 '
                                          'last:border-0 pr-5"]/p').text
    except NoSuchElementException:
        energy = ''
    description = page.find_element(By.XPATH, '//p[@class="text-gray-700 py-3 mt-3"]').text,

    try:
        allergens = page.find_element(By.XPATH, '//div[contains(@class, "flex text-gray-1000")]/p['
                                                '2]').text,
    except NoSuchElementException:
        allergens = ''
#     disclaimer = page.find_element(By.XPATH, '//span[@class="web-1wnxtfh"]').text,

    # CDriver().driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)

    # ingredients
    ingredients_list = []
    try:
        ingredients_raw = CDriver().driver.find_elements(By.XPATH, "//section[@class='w-full "
                                                                   "md:w-1/2 px-3 py-3']/ul["
                                                                   "@class='pl-6']/li[@class='text-gray-1000 mb-5 list-disc last:mb-0']/p")
        for ingredient in ingredients_raw:
            ing_name = ingredient.text
            ing_name = ing_name + ', '
            ingredients_list.append(ing_name)
        # print(ingredients_list)
    except NoSuchElementException:
        ingredients_list = ['No ingredients provided']

    # utensils
    utensils_list = []
    try:
        utensils_raw = CDriver().driver.find_elements(By.XPATH, "//section[@class='w-full md:w-1/2 px-3 py-3 "
                                                   "pt-5 mt-5 border-t md:mt-0 md:border-l "
                                                   "md:border-t-0 border-gray-300']/ul[@class='pl-6']/li[@class='text-gray-1000 mb-5 list-disc last:mb-0']/p")

        for item in utensils_raw:
            utensil = item.text
            utensil = utensil + ', '
            utensils_list.append(utensil)
    except NoSuchElementException:
        utensils_list = ['No utensils specified']

    # ****** Nutrition **** Click button to expand data-testid="tab__nutrition-facts"
    try:
        CDriver().driver.find_element(By.XPATH, '//button['
                                             '@data-testid="tab__nutrition-facts"]').click()

        # calories = CDriver().driver.find_element(By.XPATH, "//div[@class='flex mb-3']/p["
        #                                                    "@class='font-bold ml-1']").text
        # Nutrients
        nutrients_list = []
        nutrients_raw = CDriver().driver.find_elements(By.XPATH,
                                                       "//tbody/tr[@class='border-b "
                                                       "border-gray-300 last:border-b-0']/td[@class='py-2'][1]/p[@class='text-gray-700']")
        for nutrient in nutrients_raw:
            nut_name = nutrient.text
            nutrients_list.append(nut_name)
        # print(nutrients_list)
        # Serving
        serving_list = []
        serving_raw = CDriver().driver.find_elements(By.XPATH, "//tbody/tr[@class='border-b border-gray-300 last:border-b-0']/td[@class='py-2'][2]/p[@class='font-bold text-gray-1000']")
        for serving in serving_raw:
            numb = serving.text
            serving_list.append(numb)
        # print(serving_list)

        nutrition = dict(zip(nutrients_list, serving_list))
        # print(nutrition)
    except NoSuchElementException:
        nutrition = {'none': 'No nutrition specified'}

    # ****** recipe **** Click button to expand data-testid="tab__recipe" **************
    try:
        CDriver().driver.find_element(By.XPATH, '//button['
                                                '@data-testid="tab__recipe"]').click()

        # Step numbers
        step_list = []
        step_raw = CDriver().driver.find_elements(By.XPATH, "//div[@class='mt-5 w-full text-left flex flex-col md:w-5/12 md:mt-0']/div[@class='font-bold mb-3 text-gray-1000']")
        for number in step_raw:
            num = number.text
            step_list.append(num)
        # print(step_list)
        # Step descriptions
        steptext_list = []
        steptext_raw = CDriver().driver.find_elements(By.XPATH, "//div[@class='mt-5 w-full text-left flex flex-col md:w-5/12 md:mt-0']/div[@class='text-gray-700']")
        for p in steptext_raw:
            ptext = p.text
            steptext_list.append(ptext)
        # print(steptext_list)
        instructions = dict(zip(step_list, steptext_list))
    except NoSuchElementException:
        instructions = {'none': 'Not specified'}

#
    # convert tuple values to string before making Dict
    keywords = ['name', 'sub_name', 'url', 'cook_time', 'energy', 'description',
                'allergens', 'ingredients', 'utensils', 'nutrition',
                'instructions'
                ]
    values_tp.extend((name, name2, page_url, cook_time, energy, description,
                      allergens, ingredients_list, utensils_list,
                      ))
    for value in values_tp:
        i = ''.join(value)
        values_list.append(i)
#
#     # Adding extra dicts to values_list
    values_list.extend((nutrition, instructions))
#     # Making Dict with product details
    product_dict = dict(zip(keywords, values_list))
    product.append(product_dict)
#
#     # Saving files
#     if pdf_url is not None:
#         pdf_name = "results/chefs_plate/pdfs/" + values_list[0] + ".pdf"
#         response = urllib.request.urlopen(pdf_url)
#         file = open(pdf_name, 'wb')
#         file.write(response.read())
#         file.close()
#
#
print(product)
with open('results/good_food/gf_output.json', 'w') as f:
    f.write(json.dumps(product))



