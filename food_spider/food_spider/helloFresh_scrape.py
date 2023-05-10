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

############ Hello Fresh selinum test ###################
# url = 'https://www.hellofresh.ca/menus?locale=en-CA'
#
# urls = []
#
# CDriver().driver.delete_all_cookies()
# CDriver().driver.get(url)
# print(url)
# input("Scroll page down and wait for pop-up, Press Enter to continue...")
#  # go into each menu item (open modal) and get the detail information href of each
# x = CDriver().driver.find_elements(By.CSS_SELECTOR,
#                                               'div[data-test-id="recipe-card-component"]')
# print(len(x))
# input("Scroll page down and wait for pop-up, Press Enter to continue...")
# for my_elem in x:
#     # urls.append(my_elem.get_attribute("href"))
#
#     # click on recipe
#     my_elem.click()
#     # get link of recipe details
#     link = WebDriverWait(CDriver().driver, 5).until(EC.visibility_of_element_located(
#         (By.CSS_SELECTOR, 'div[data-test-id="recipe-details-card"]')))
#     link2 = WebDriverWait(CDriver().driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ReactModal__Content--after-open")))
#     h2text = link2.find_element(By.CSS_SELECTOR, '.web-q5jmhc')
#     urltext = h2text.get_attribute("href")
#     urls.append(urltext)
#     print(urltext)
#     # go back
#     time.sleep(3)
#     link.click()
#
# urls = list(set(urls))
# print(urls)

######### Chefs plate selinium test ###################
url = 'https://www.chefsplate.com/weekly-menu'

urls = []

CDriver().driver.delete_all_cookies()
CDriver().driver.get(url)
print(url)
input("Scroll page down and wait for pop-up, Press Enter to continue...")
# # go into each menu item (open modal) and get the detail information href of each
# Get first slider
slider = CDriver().driver.find_element(By.XPATH, "//div[@class='swiper-wrapper'][1]")
# x = []
x= slider.find_elements(By.CSS_SELECTOR, ".web-1c82rjx")
# for elem in element:
#     x.append(elem)
##################### only for testing ##########################
# x = []
# xx = CDriver().driver.find_element(By.XPATH, '//a[@class="web-1c82rjx"][1]')

# x.append(xx)
##########################
print(len(x))
input("Scroll page down and wait for pop-up, Press Enter to continue...")
for my_elem in x:

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
        By.CSS_SELECTOR, ".web-1lanr3s")))

    name = page.find_element(By.XPATH, '//h1[@class="web-xlhhyt"]').text,
    name2 = page.find_element(By.XPATH, '//h3[@class="web-1ilptws"]').text,
    page_url = url
    # pdf_url = CDriver().driver.find_element(By.XPATH, '//a[@class="web-l1teuz"]').get_attribute(
    #     "href")
    try:
        pdf_url = CDriver().driver.find_element(By.XPATH, '//a[@class="web-l1teuz"]').get_attribute("href")
    except NoSuchElementException:
        pdf_url = None
    cook_time = page.find_element(By.XPATH, '//div[@data-test-id="prep-time"]').text,
    energy = page.find_element(By.XPATH, '//div[@data-recipe-energy="true"]').text,
    description = page.find_element(By.XPATH, '//div/p[@class="web-1u68b9m"]').text,
    try:
        allergens = page.find_element(By.XPATH, '//span[@data-test-id="recipe-allergens"]').text,
    except NoSuchElementException:
        allergens = ''
    disclaimer = page.find_element(By.XPATH, '//span[@class="web-1wnxtfh"]').text,

    # *******Get nutrients per serving and 100g
    # Nutrients
    nutrients_list = []
    nutrients_raw = CDriver().driver.find_elements(By.XPATH, '//small[@class="web-14d5zh9"]/strong')
    for nutrient in nutrients_raw:
        nut_name = nutrient.text
        nutrients_list.append(nut_name)
    # print(nutrients_list)
    # Serving
    serving_list = []
    serving_raw = CDriver().driver.find_elements(By.XPATH, '//div[@class="web-dxsv06"]/span')
    for serving in serving_raw:
        numb = serving.text
        serving_list.append(numb)
    # print(serving_list)
    # Per 100g
    per100_list = []
    per100_raw = CDriver().driver.find_elements(By.XPATH, '//div[@data-test-id="nutrition-per-100g"]')
    for item in per100_raw:
        numb2 = item.text
        per100_list.append(numb2)
    # print(per100_list)
    # MAke dictionaries for *Serving and *per100g
    nutrition_serving = dict(zip(nutrients_list, serving_list))
    nutrition_per100 = dict(zip(nutrients_list, per100_list))

    # *****Get Ingredients
    # ingredients
    ingredients_list = []
    ingredients_raw = CDriver().driver.find_elements(By.XPATH, '//p[@class="web-1uk1gs8"]')
    for ingredient in ingredients_raw:
        ing_name = ingredient.text
        ingredients_list.append(ing_name)
    # print(ingredients_list)
    # Ingredient values
    ingvalues_list = []
    ingvalues_raw = CDriver().driver.find_elements(By.XPATH, '//p[@class="web-x8zzfc"]')
    for value in ingvalues_raw:
        value_num = value.text
        ingvalues_list.append(value_num)
    # print(ingvalues_list)
    # Make dict with ingredients and values
    ingredient_values = dict(zip(ingredients_list, ingvalues_list))

    # ******Recipe Steps **** Click button to expand data-test-id="toggle-cooking-steps"
    # CDriver().driver.find_element(By.XPATH, '//button[@data-test-id="toggle-cooking-steps"]').click()
    # Needs to scroll down to make the button visible and then scroll again to get paragraphs
    CDriver().driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    link = WebDriverWait(CDriver().driver, 2).until(EC.visibility_of_element_located(
        (By.XPATH, '//button[@data-test-id="toggle-cooking-steps"]')))
    link.click()
    CDriver().driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Step numbers
    step_list = []
    step_raw = CDriver().driver.find_elements(By.XPATH, '//span[@class="web-sd7euz"]')
    for number in step_raw:
        num = number.text
        step_list.append(num)
    # print(step_list)
    # Step descriptions
    steptext_list = []
    steptext_raw = CDriver().driver.find_elements(By.XPATH, '//div[@class="web-1hhw9qn"]/p')
    for p in steptext_raw:
        ptext = p.text
        steptext_list.append(ptext)
    # print(steptext_list)
    # print(CDriver().driver.find_element(By.XPATH, '//h3[@class="web-uymkwo"]').text)
    # MAke Dict of steps
    instructions = dict(zip(step_list, steptext_list))

    # convert tuple values to string before making Dict
    keywords = ['name', 'sub_name', 'url', 'pdf_url', 'cook_time', 'energy', 'description',
                'allergens', 'disclaimer',
                'nutrition_serving', 'nutrition_per100', 'ingredient_values', 'instructions']
    values_tp.extend((name, name2, page_url, pdf_url, cook_time, energy, description,
                      allergens, disclaimer))
    for value in values_tp:
        i = ''.join(value)
        values_list.append(i)

    # Adding extra dicts to values_list
    values_list.extend((nutrition_serving, nutrition_per100, ingredient_values, instructions))
    # Making Dict with product details
    product_dict = dict(zip(keywords, values_list))
    product.append(product_dict)

    # Saving files
    if pdf_url is not None:
        pdf_name = "results/chefs_plate/pdfs/" + values_list[0] + ".pdf"
        response = urllib.request.urlopen(pdf_url)
        file = open(pdf_name, 'wb')
        file.write(response.read())
        file.close()


print(product)
with open('results/chefs_plate/cp_output.json', 'w') as f:
    f.write(json.dumps(product))



