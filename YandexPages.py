from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class YandexMainPage:
    SEARCH_FIELD = (By.ID, 'text')
    SUGGEST_TABLE = (By.CSS_SELECTOR, '.mini-suggest__popup')
    SEARCH_RESULTS = (By.CSS_SELECTOR, '.search3__button')
    IMAGE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Картинки"]')
    MENU_BUTTON = (By.CSS_SELECTOR, '[href="https://yandex.ru/all"]')
    IMAGE_LINK = (By.CSS_SELECTOR, 'a[href="https://yandex.ru/images/"]')

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get('https://ya.ru/')

    def is_search_loaded(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_FIELD)
        )

    def search(self, text):
        search_field = self.driver.find_element(*self.SEARCH_FIELD)
        search_field.clear()
        search_field.send_keys(text)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SUGGEST_TABLE)
        )

    def press_enter(self):
        self.driver.find_element(*self.SEARCH_RESULTS).submit()

    def is_menu_loaded(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MENU_BUTTON)
        )

    def open_menu(self):
        self.driver.find_element(*self.MENU_BUTTON).click()

    def open_images_page(self):
        self.driver.find_element(*self.IMAGE_BUTTON).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        return WebDriverWait(self.driver, 10).until(EC.url_contains('https://yandex.ru/images/'))

    def is_page_loaded(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.IMAGE_LINK)
        )


class YandexImagesPage:
    CATEGORY_TITLE = (By.CSS_SELECTOR, '.PopularRequestList-SearchText')
    SEARCH_ROW = (By.CSS_SELECTOR, 'div.Root_inited')
    SEARCH_RESULTS = (By.CSS_SELECTOR, '.serp-controller__content .a11y-hidden')
    FIRST_CATEGORY = (By.CSS_SELECTOR, '.PopularRequestList-Item:first-child')
    IMAGE = (By.CSS_SELECTOR, '.MMImage-Origin')
    FIRST_IMAGE = (By.CSS_SELECTOR, '.serp-item_pos_0 .serp-item__link')
    NEXT_BUTTON = (By.CSS_SELECTOR, '.MediaViewer_theme_fiji-ButtonNext')
    PREV_BUTTON = (By.CSS_SELECTOR, '.MediaViewer_theme_fiji-ButtonPrev')

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get('https://yandex.ru/images/')

    def is_loaded(self):
        return WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE)
        )

    def open_category(self):
        category = self.driver.find_element(*self.FIRST_CATEGORY).text
        self.driver.find_element(*self.FIRST_CATEGORY).click()
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located(self.SEARCH_RESULTS)
        )
        return category in self.driver.find_element(*self.SEARCH_ROW).get_attribute('data-state')

    def open_first_image(self):
        self.driver.find_element(*self.FIRST_IMAGE).click()
        ActionChains(self.driver).context_click(self.driver.find_element(By.CSS_SELECTOR, '.MMImage-Origin')).perform()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NEXT_BUTTON)
        )
        WebDriverWait(self.driver, 1000).until_not(
            EC.text_to_be_present_in_element_attribute(locator=(By.CSS_SELECTOR, '.MMImage-Origin'), attribute_='src',
                                                       text_='https://avatars.mds.yandex.net/')
        )

    def press_next(self):
        self.driver.find_element(*self.NEXT_BUTTON).click()
        ActionChains(self.driver).context_click(self.driver.find_element(By.CSS_SELECTOR, '.MMImage-Origin')).perform()
        WebDriverWait(self.driver, 1000).until_not(
            EC.text_to_be_present_in_element_attribute(locator=(By.CSS_SELECTOR, '.MMImage-Origin'), attribute_='src',
                                                       text_='https://avatars.mds.yandex.net/')
        )

    def press_prev(self):
        self.driver.find_element(*self.PREV_BUTTON).click()
        ActionChains(self.driver).context_click(self.driver.find_element(By.CSS_SELECTOR, '.MMImage-Origin')).perform()
        WebDriverWait(self.driver, 1000).until_not(
            EC.text_to_be_present_in_element_attribute(locator=(By.CSS_SELECTOR, '.MMImage-Origin'), attribute_='src',
                                                       text_='https://avatars.mds.yandex.net/')
        )
