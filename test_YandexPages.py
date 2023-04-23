import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from YandexPages import YandexMainPage, YandexImagesPage


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()


@pytest.fixture()
def yandex_main_page(browser):
    yandex_main_page = YandexMainPage(browser)
    yandex_main_page.load()
    assert yandex_main_page.is_search_loaded()
    yield yandex_main_page


@pytest.fixture()
def yandex_images_page(browser):
    yandex_images_page = YandexImagesPage(browser)
    yandex_images_page.load()
    # assert yandex_images_page.is_loaded()
    yield yandex_images_page


def test_search_yandex(yandex_main_page):
    logging.info('Performing search for "Тензор"')
    yandex_main_page.search('Тензор')
    yandex_main_page.press_enter()
    assert 'https://yandex.ru/search/' in yandex_main_page.driver.current_url
    links = yandex_main_page.driver.find_elements(By.CSS_SELECTOR, '.organic__url')
    assert any('tensor.ru' in link.get_attribute('href') for link in links)
    logging.info('Test passed successfully')


def test_open_images_page(yandex_main_page):
    logging.info('Performing attempt to load Image Page')
    yandex_main_page.search(' ')
    assert yandex_main_page.is_menu_loaded()
    yandex_main_page.open_menu()
    assert yandex_main_page.open_images_page()
    logging.info('Test passed successfully')


def test_open_first_image(yandex_images_page):
    logging.info('Performing attempt to open first category')
    assert yandex_images_page.is_loaded()
    assert yandex_images_page.open_category()
    logging.info('Performing attempt to open first picture')
    yandex_images_page.open_first_image()
    current_image_url = yandex_images_page.driver.find_element(By.CSS_SELECTOR, '.MMImage-Origin').get_attribute('src')
    yandex_images_page.press_next()
    next_image_url = yandex_images_page.driver.find_element(By.CSS_SELECTOR, '.MMImage-Origin').get_attribute('src')
    yandex_images_page.press_prev()
    prev_image_url = yandex_images_page.driver.find_element(By.XPATH, '//img[@class="MMImage-Origin"]').get_attribute(
        'src')
    assert current_image_url == prev_image_url
    assert current_image_url != next_image_url
    logging.info('Test passed successfully')