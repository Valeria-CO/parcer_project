from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from datetime import date, timedelta


def scrape_data(city:str):
    today =date.today()
    tomorrow = today + timedelta(days=1)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.booking.com/")
    wait.until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, "body")))

    try:
        cancel_button = wait.until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[aria-label='Скрыть меню входа в аккаунт.']")
        ))
        cancel_button.click()
    except TimeoutException:
        pass

    city_in = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[data-destination='1']")))
    city_in.send_keys(city)
    driver.find_element(By.CSS_SELECTOR, "button[data-testid='searchbox-dates-container']").click()
    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "span[data-date]")))
    first_date = driver.find_element(By.CSS_SELECTOR, "span[data-date='{}']".format(today))
    first_date.click()
    second_date = driver.find_element(By.CSS_SELECTOR, "span[data-date='{}']".format(tomorrow))
    second_date.click()

    submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit.click()

    wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid=property-card]")))
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid=property-card]")
    hotels = []

    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "div[data-testid=title]")
            url = card.find_element(By.CSS_SELECTOR, "a[data-testid=title-link]").get_attribute('href')
            price = card.find_element(By.CSS_SELECTOR, "span[data-testid=price-and-discounted-price]")
            hotels.append({'title.text': title.text, 'url': url, 'price': price.text})
        except Exception as e:
            print("error processing card", e)

    driver.quit()
    return hotels



