import sqlite3
import time
import requests

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from output import write_result


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

    def get_data(self, f , l):
        """get data tobe stored"""
        followers_count = f
        like_count = l
        author_username = self.driver.find_element(By.XPATH, "//h1[@data-e2e='user-title']").text
        following_count = self.driver.find_element(By.XPATH, "//strong[@title='Following']").text
        return (author_username, followers_count, following_count, like_count)

    def analyze_data(self):
        """
        this method will check for at least 100k followers and 1 million likes to avoid unnecessary data
        also export data in csv
        """
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//strong[@data-e2e='followers-count']"))
            )
            time.sleep(3)
            self.driver.implicitly_wait(10)
            followers = self.driver.find_element(By.XPATH, "//strong[@data-e2e='followers-count']")
            total_f = followers.text
            likes = self.driver.find_element(By.XPATH, "//strong[@data-e2e='likes-count']")
            total_l = likes.text
            if total_f.find('K') >= 0 and total_l.find('M') >= 0:
                # result = self.get_data(total_f, total_l)
                author_username = self.driver.find_element(By.XPATH, "//h1[@data-e2e='user-title']").text
                following_count = self.driver.find_element(By.XPATH, "//strong[@title='Following']").text
                result = [author_username, total_f, following_count, total_l]
                # self.db_handling(result)
                write_result(result)
            else:
                print('could not fill the requirements')


        except:
            print('somethign wrong happend')

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
        "this method will work only for keyword search"
        key_list = ["places to visit", "places to travel", "travel hacks","beautiful destinations", "places that don't feel real"]
        for kw in key_list:
            self.search_with_keyword(kw)
            time.sleep(3)
            self.driver.implicitly_wait(10)
            self.scrap_links()

    def db_handling(self, data):
        connection = sqlite3.connect('seleniumdb.db')
        cursor = connection.cursor()
        print('inside db 1')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS information(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            authorusername TEXT NOT NULL,       
            followerscount TEXT NOT NULL,
            followingcount TEXT NOT NULL,
            likecount TEXT NOT NULL,

        )
        ''')
        print('inside db 2')
        # now insert data
        author_username, followers_count, following_count, like_count = data
        # here first email, phone specifying the column, ? are specifying as the placeholder of actual data, last email and phone are actuall data which replace ? and ?
        cursor.execute('''
                INSERT INTO information (authorusername, followerscount, followingcount, likecount)
                VALUES (?, ?, ?, ?)
                ''', (author_username, followers_count, following_count, like_count))
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
        time.sleep(1000)


if __name__ == '__main__':
    bot = WithUcScraper()
    bot.run()
