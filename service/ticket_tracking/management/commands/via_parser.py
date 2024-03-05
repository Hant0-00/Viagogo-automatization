import re
from _decimal import Decimal
from datetime import datetime, timezone

from django.core.management import BaseCommand
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ticket_tracking.models import Event


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Ініціалізуйте веб-драйвер (ви повинні встановити веб-драйвер для вашого браузера)
        driver = uc.Chrome()

        # Відкрийте сторінку входу
        driver.get(
            'https://account.viagogo.com/login/v2?ReturnUrl=%2Fauthorize%3Fclient_id%3Diqgpy5KIA4HZx0QBRFlb%26response_type%3Dcode%26scope%3Dinternal%2Bread%253Auser%2Bwrite%253Auser%2Bread%253Asellerlistings%2Bwrite%253Asellerlistings%2Bwrite%253Arequestedevents%2Bwrite%253Asales%2Bread%253Asales%2Bwrite%253Aworkitems%2Bread%253Aworkitems%2Bim%253Acanuse%26redirect_uri%3Dhttps%253A%252F%252Finv.viagogo.com%252Flogin%252Fcallback')

        time.sleep(1)

        # Заповніть форму входу (замініть 'your_username' та 'your_password' на ваші реальні облікові дані)
        username_field = driver.find_element(By.ID, 'Login_UserName')
        username_field.send_keys('linchenko1995@gmail.com')
        password_field = driver.find_element(By.ID, 'Login_Password')
        password_field.send_keys('Z2LE3m0zv@]c<[kP$o[B')

        # Натисніть кнопку входу
        login_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn.bk.js-nodoubleclick'))
        )
        login_button.click()

        # # Очікуйте, поки сторінка користувача не завантажиться
        time.sleep(1)
        driver.get('https://inv.viagogo.com/Listings')
        time.sleep(2)

        elements = driver.find_elements(By.CLASS_NAME, 'i-chevron-right')
        sector = driver.find_elements(By.XPATH, '//div[contains(@class, "h xs mbxxs t0 w100 ellip")]')
        number_event = driver.find_elements(By.XPATH, '//span[contains(@class, "t xs cGry4 w100 ellip")]')
        data_time = driver.find_elements(By.XPATH, '//div[contains(@class, "t xs mbxxs nowrap")]')
        location = driver.find_elements(By.XPATH, '//div[contains(@class, "t xxs cGry4 w100 ellip")]')
        plus_click = driver.find_elements(By.XPATH, '//i[contains(@class, "t m i-magnify cGry4")]')

        full_list = []

        for i in range(0, len(elements)):
            driver.execute_script("arguments[0].scrollIntoView();", elements[i])
            # elements[i].click()
            driver.execute_script("arguments[0].click();", elements[i])
            time.sleep(1)

            # Locate the table element by class name
            table = driver.find_element(By.CLASS_NAME, 'js-listing-container.expanded')
            table_rows = table.find_elements(By.TAG_NAME, "tr")

            for row in table_rows:
                table_data = row.find_elements(By.TAG_NAME, "td")

                try:
                    check_box_element = row.find_element(By.CLASS_NAME, "publishedCol")
                    check_box = check_box_element.find_element(By.TAG_NAME, 'input').is_selected()
                    edit_listing = row.find_element(By.CLASS_NAME, "t.m.i-pencil.cGry4")

                    # Чекає поки модальне модальне вікно стане видимим
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.invisibility_of_element_located((By.ID, 'modal')))
                    driver.execute_script("arguments[0].click();", edit_listing)
                    # -----------------#

                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, 'cfix'))
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, 'input.js-restriction-on-use-listing-note-check'))
                    )

                    # Знайдіть елемент, до якого ви хочете прокрутити
                    element_to_scroll_to = driver.find_element(By.CLASS_NAME, "cfix")

                    driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll_to)
                    time.sleep(0.5)

                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(@id, "js-listingId")]'))
                    )
                    listing_id = element.get_attribute("innerText")

                    # Знаходимо всі чекбокси, які вибрані (checked)
                    selected_checkboxes = driver.find_elements(By.XPATH,
                                                               '//input[@name="Listing.ListingNoteIds" and @checked]')

                    features_list = []
                    for check in selected_checkboxes:
                        label_text = check.find_element(By.XPATH, 'following-sibling::label').text
                        features_list.append(label_text)

                    driver.execute_script("arguments[0].scrollIntoView();",
                                          driver.find_element(By.CLASS_NAME, 'fg.rel'))

                    # Очікуйте, доки елемент не стане видимим
                    cancel_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//button[text()="Cancel"]'))
                    )

                    cancel_button.click()
                    time.sleep(2)
                    #----------- Блок отримання номера білета у списку ---------
                    driver.execute_script("arguments[0].click();", plus_click[i])
                    time.sleep(2)
                    wait = WebDriverWait(driver, 10)
                    select_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//select[contains(@class, "s")]')))

                    # Ініціалізація об'єкта Select
                    select = Select(select_element)

                    # Очікування наявності варіантів у випадаючому списку
                    wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, "//select[@id='mDataSectionFilter']/option")))

                    # index = table_rows.index(row) * -1
                    # print(index)
                    # opt = select.options[index]
                    select.select_by_visible_text(row.text.split("\n")[0])
                    my_table = driver.find_element(By.XPATH, '//table[contains(@class, "w100 bdr0 bGry9 fixed")]')
                    all_tr = my_table.find_elements(By.TAG_NAME, "tr")
                    tr_list = [tr.get_attribute("outerHTML") for tr in all_tr]

                    for test in tr_list:
                        if f'data-id="{listing_id}"' in test:
                            bot = tr_list.index(test) + 1

                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//div[contains(@class, "close modal-close i-remove")]')))

                    driver.execute_script("arguments[0].click()", driver.find_element(
                        By.XPATH, '//div[contains(@class, "close modal-close i-remove")]'))

                except NoSuchElementException:
                    check_box = False

                row_data = []

                # Отримання всіх number_event
                text = driver.execute_script("return arguments[0].innerText;", number_event[i])
                pattern = re.compile(r'\[(\d+)\]')

                # Пошук у тексті за допомогою регулярного виразу
                match = pattern.search(text)

                # -----------------------------#

                for data in table_data:
                    row_data.append(data.text)
                if len(row_data) > 0:
                    Event.objects.create(event=sector[i].text.replace(number_event[i].text, '').strip(),
                                         data_time=datetime.strptime(data_time[i].text, "%a %b %d %Y %H:%M").replace(tzinfo=timezone.utc),
                                         location=location[i].text,
                                         number_event=int(match.group(1)),
                                         announcement_number=int(listing_id),
                                         sector=row_data[1],
                                         ticket_quantity=int(row_data[7]),
                                         features=str(features_list),
                                         state=str(check_box),
                                         net_price=Decimal(row_data[6][1::]),
                                         price=Decimal(row_data[5][1::]),
                                         bot=bot)

            driver.execute_script("arguments[0].click();", elements[i])


        # Закрийте браузер
        driver.quit()
