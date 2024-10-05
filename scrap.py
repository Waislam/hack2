import sqlite3
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


class WithUcScraper:
    absolute_path = 'https://www.tiktok.com/'

    def __init__(self):
        self.driver = uc.Chrome(options=self.handle_chrome_options())

    def scroll_down(self):
        """this method will help to scroll down 500px down"""
        self.driver.execute_script("window.scrollTo(0, window.scrollY + 500)")

    def handle_chrome_options(self):
        """this method will handle all the chrome options"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("disable-notifications")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-extensions")

    def handle_login_popup(self):
        """It should handle the login popup to redirect user as a guest"""
        try:
            # self.driver.switch_to.window(window_after)
            guest = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Continue as guest')]")
            guest.click()
        except:
            print("no login popup")

    def analyze_data(self):
        """this method will check for at least 100k followers and 1 million likes to avoid unnecessary data"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//strong[@data-e2e='followers-count']"))
            )
            print('reaching here')
            followers = self.driver.find_element(By.XPATH, "//strong[@data-e2e='followers-count']").text
            likes = self.driver.find_element(By.XPATH, "data-e2e='likes-count'").text
            print(followers)
            print(likes)
            # if followers.find('K') >= 0 and likes.find('K'):
            #     total = followers.split(".")[0]
            #     print(total)
                # if total >= 100:


        except:
            print('something wrong here')

    def scrap_links(self):
        """this will scrap only links for keyword search"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//p[@class='css-2zn17v-PUniqueId etrd4pu6']")))
            self.scroll_down()
            time.sleep(3)
            self.scroll_down()
            time.sleep(3)
            self.scroll_down()
            list_of_id = []
            ids = self.driver.find_elements(By.XPATH, "//p[@class='css-2zn17v-PUniqueId etrd4pu6']")
            for id in ids:
                relative_path = id.text
                id_link = self.absolute_path + "@" + relative_path
                list_of_id.append(id_link)
            for single_id in list_of_id:
                self.driver.get(single_id)
                self.analyze_data()
        except:
            pass

    def search_with_keyword(self, kewword):
        self.driver.implicitly_wait(15)
        input_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        input_field.send_keys(kewword)
        self.driver.find_element(By.XPATH, "//div[@class='css-17iic05-DivSearchIconContainer e14ntknm8']").click()

    def key_word_scraping(self):
        kw = 'places to visit'
        self.search_with_keyword(kw)
        time.sleep(3)
        self.driver.implicitly_wait(10)
        self.scrap_links()

    def get_data(self):
        """explicitly wait for an element"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[@class='elementor-icon-list-text']")))
        email = self.driver.find_elements(By.XPATH, "//span[@class='elementor-icon-list-text']")[1].text
        phone = self.driver.find_elements(By.XPATH, "//span[@class='elementor-icon-list-text']")[0].text
        return (email, phone)

    def db_handling(self, data):
        connection = sqlite3.connect('seleniumdb.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS information(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,       
            phone TEXT NOT NULL
        )
        ''')

        # now insert data
        email, phone = data
        # here first email, phone specifying the column, ? are specifying as the placeholder of actual data, last email and phone are actuall data which replace ? and ?
        cursor.execute('''
                INSERT INTO information (email, phone)
                VALUES (?, ?)
                ''', (email, phone))
        connection.commit()  # to save data into db
        connection.close()  # close db

    def run(self):
        # self.driver.get('https://www.tiktok.com/')
        self.driver.get('https://www.tiktok.com/explore')
        self.driver.implicitly_wait(10)
        time.sleep(5)
        self.handle_login_popup()
        print('there is no login popup')
        self.key_word_scraping()
        # result = self.get_data()
        # self.db_handling(result)
        time.sleep(1000)


if __name__ == '__main__':
    bot = WithUcScraper()
    bot.run()
