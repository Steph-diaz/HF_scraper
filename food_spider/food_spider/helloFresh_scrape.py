from pathlib import Path
from cdriver import CDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import time


url = 'https://www.hellofresh.ca/menus?locale=en-CA'

urls = []

CDriver().driver.delete_all_cookies()
CDriver().driver.get(url)
print(url)
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
        (By.CSS_SELECTOR, 'div[data-test-id="recipe-details-card"]')))
    link2 = WebDriverWait(CDriver().driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ReactModal__Content--after-open")))
    h2text = link2.find_element(By.CSS_SELECTOR, '.web-q5jmhc')
    urltext = h2text.get_attribute("href")
    urls.append(urltext)
    print(urltext)
    # go back
    time.sleep(3)
    link.click()

urls = list(set(urls))
print(urls)
