import re
import selenium
import telebot
from _decimal import Decimal
from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
import time
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

from core import settings
from ticket_tracking.models import Event


class Command(BaseCommand):

    def handle(self, *args, **options):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = uc.Chrome(options=chrome_options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                # platform="Win32",
                platform="Linux x86_64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        # Відкрийте сторінку входу
        driver.get(
            'https://account.viagogo.com/login/v2?ReturnUrl=%2Fauthorize%3Fclient_id%3Diqgpy5KIA4HZx0QBRFlb%26response_type%3Dcode%26scope%3Dinternal%2Bread%253Auser%2Bwrite%253Auser%2Bread%253Asellerlistings%2Bwrite%253Asellerlistings%2Bwrite%253Arequestedevents%2Bwrite%253Asales%2Bread%253Asales%2Bwrite%253Aworkitems%2Bread%253Aworkitems%2Bim%253Acanuse%26redirect_uri%3Dhttps%253A%252F%252Finv.viagogo.com%252Flogin%252Fcallback')

        time.sleep(1)

        # Заповнення форми входу
        username_field = driver.find_element(By.ID, 'Login_UserName')
        username_field.send_keys('linchenko1995@gmail.com')
        password_field = driver.find_element(By.ID, 'Login_Password')
        password_field.send_keys('66&n^Z2_9Fuv%v7R#*JJpb4&P5Sh-i9B')

        # Натискання кнопки входу
        login_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn.bk.js-nodoubleclick'))
        )
        login_button.click()
        time.sleep(1)
        driver.get('https://inv.viagogo.com/Listings')
        time.sleep(2)

        elements = driver.find_elements(By.CLASS_NAME, 'i-chevron-right')
        name_event = driver.find_elements(By.XPATH, '//div[contains(@class, "h xs mbxxs t0 w100 ellip")]')
        number_event = driver.find_elements(By.XPATH, '//span[contains(@class, "t xs cGry4 w100 ellip")]')
        data_time = driver.find_elements(By.XPATH, '//div[contains(@class, "t xs mbxxs nowrap")]')
        location = driver.find_elements(By.XPATH, '//div[contains(@class, "t xxs cGry4 w100 ellip")]')
        plus_click = driver.find_elements(By.XPATH, '//i[contains(@class, "t m i-magnify cGry4")]')
        wait = WebDriverWait(driver, 10)

        for i in range(0, len(elements)):
            driver.execute_script("arguments[0].scrollIntoView();", elements[i])
            driver.execute_script("arguments[0].click();", elements[i])
            time.sleep(1)
            table = driver.find_element(By.CLASS_NAME, 'js-listing-container.expanded')
            table_rows = table.find_elements(By.TAG_NAME, "tr")[1::]
            test_dict = {}
            for test_row in table_rows:
                test_sector = test_row.find_element(By.XPATH, './/div[contains(@class, "t xs absl t0 w100 ellip")]')
                listing_id = test_row.get_attribute("data-id")
                test_dict[listing_id]=test_sector.text

            for key, value in test_dict.items():

                try:
                    event = Event.objects.get(announcement_number=key)
                    driver.execute_script("arguments[0].click();", plus_click[i])
                    time.sleep(2)

                    select_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//select[contains(@class, "s")]')))

                    wait.until(EC.visibility_of(select_element))

                    driver.execute_script("arguments[0].click();", select_element)
                    # Ініціалізація об'єкта Select
                    select = Select(select_element)

                    # Очікування наявності варіантів у випадаючому списку
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='mDataSectionFilter']/option")))

                    select.select_by_visible_text(value)
                    my_table = driver.find_element(By.XPATH, '//table[contains(@class, "w100 bdr0 bGry9 fixed")]')
                    all_tr = my_table.find_elements(By.TAG_NAME, "tr")
                    tr_list = [tr.get_attribute("outerHTML") for tr in all_tr]
                    if f'data-id="{event.announcement_number}"' not in tr_list[0] and event.state != 'False' and event.source_price:
                        list_min_price = []
                        for tr_test in all_tr:
                            price_text = tr_test.find_element(By.XPATH, './/td[contains(@data-edit-field, "WebsitePriceVal")]').text[1:]
                            data_id = tr_test.get_attribute("data-id")
                            if data_id == str(event.announcement_number):
                                break
                            elif data_id == '':
                                list_min_price.append(price_text)
                        min_price_in_site = 0
                        for min_price in list_min_price:
                            if float(min_price) > float(event.min_price):
                                min_price_in_site = float(min_price)
                                break
                        if min_price_in_site:
                            tr_element = driver.find_element(By.XPATH, f'//tr[@data-id="{event.announcement_number}"]')
                            td_element = tr_element.find_element(By.XPATH, './/td[@data-edit-field="WebsitePriceVal"]')

                            driver.execute_script("arguments[0].click();", td_element)

                            input_element = wait.until(EC.visibility_of_element_located(
                                (By.XPATH,
                                 '//td[@data-edit-field="WebsitePriceVal"]//div[@class="rel"]/input[@class="m0"]')))

                            driver.execute_script("arguments[0].value = '';", input_element)
                            time.sleep(2)
                            key = float(min_price_in_site) - 0.01
                            input_element.send_keys(f"{key}+")
                            input_element.send_keys(Keys.ENTER)

                    """ Блок логіки збільшення ціни """
                    if f'data-id="{event.announcement_number}"' in tr_list[0] and len(tr_list) > 1 and event.source_price:
                        price_my_ticket = all_tr[0].find_element(By.XPATH, './/td[contains(@data-edit-field, "WebsitePriceVal")]').text[1:]
                        price_second_ticket = all_tr[1].find_element(By.XPATH, './/td[contains(@data-edit-field, "WebsitePriceVal")]').text[1:]

                        if float(float(price_second_ticket) - float(price_my_ticket)) > 0.01:
                            print('2-й сценарій')
                            td_element = driver.find_element(By.XPATH, '//td[@class="txtc w15 editable"]')
                            driver.execute_script("arguments[0].click();", td_element)
                            time.sleep(4)

                            input_element = wait.until(EC.visibility_of_element_located(
                                (By.XPATH,
                                 '//td[@data-edit-field="WebsitePriceVal"]//div[@class="rel"]/input[@class="m0"]')))

                            driver.execute_script("arguments[0].value = '';", input_element)

                            key = float(price_second_ticket) - 0.01

                            input_element.send_keys(f"{key}+")
                            input_element.send_keys(Keys.ENTER)

                    if len(tr_list) == 1 and event.source_price:
                        td_element = driver.find_element(By.XPATH, '//td[@class="txtc w15 editable"]')
                        driver.execute_script("arguments[0].click();", td_element)


                        input_element = wait.until(EC.visibility_of_element_located(
                            (By.XPATH,
                                '//td[@data-edit-field="WebsitePriceVal"]//div[@class="rel"]/input[@class="m0"]')))

                        driver.execute_script("arguments[0].value = '';", input_element)

                        key = event.max_price
                        input_element.send_keys(f"{key}+")
                        input_element.send_keys(Keys.ENTER)

                    wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(@class, "close modal-close i-remove")]')))
                    driver.execute_script("arguments[0].click()", driver.find_element(
                        By.XPATH, '//div[contains(@class, "close modal-close i-remove")]'))

                except ObjectDoesNotExist:
                    break

            time.sleep(1)
            # Знаходження таблиці
            table = driver.find_element(By.CLASS_NAME, 'js-listing-container.expanded')
            table_rows = table.find_elements(By.TAG_NAME, "tr")[1::]

            for row in table_rows:
                listing_id = row.get_attribute("data-id")
                state_check_box = row.find_element(By.XPATH, f'//input[contains(@id, "publish{listing_id}")]').is_selected()
                edit_listing = row.find_element(By.CLASS_NAME, "t.m.i-pencil.cGry4")
                sector = row.find_element(By.XPATH, './/div[@class="t xs absl t0 w100 ellip"]').text
                ticket_quantity = int(row.find_element(By.XPATH, './/td[@data-edit-field="AvailableTickets"]').text)
                price = Decimal(row.find_element(By.XPATH, './/td[@data-edit-field="WebsitePriceVal"]').text[1::])
                net_price = Decimal(row.find_element(By.XPATH, './/td[@data-edit-field="ProceedsVal"]').text[1::])


                # Чекає поки модальне модальне вікно стане видимим

                driver.execute_script("arguments[0].click();", edit_listing)
                wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="l noclose js-modal-size"]')))
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
                time.sleep(1)
                #----------- Блок отримання номера білета у списку ---------
                driver.execute_script("arguments[0].click();", plus_click[i])
                time.sleep(2)

                select_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//select[contains(@class, "s")]')))

                # Ініціалізація об'єкта Select
                driver.execute_script("arguments[0].click();", select_element)

                select = Select(select_element)
                # Очікування наявності варіантів у випадаючому списку
                wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//select[@id='mDataSectionFilter']/option")))

                select.select_by_visible_text(sector)
                table_all_ticket = driver.find_element(By.XPATH, '//table[contains(@class, "w100 bdr0 bGry9 fixed")]')
                all_tr = table_all_ticket.find_elements(By.TAG_NAME, "tr")
                tr_list = [tr.get_attribute("outerHTML") for tr in all_tr]

                for test in tr_list:
                    if f'data-id="{listing_id}"' in test:
                        bot = tr_list.index(test) + 1

                wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "close modal-close i-remove")]')))
                time.sleep(1)
                driver.execute_script("arguments[0].click()", driver.find_element(
                    By.XPATH, '//div[contains(@class, "close modal-close i-remove")]'))



                # Отримання всіх number_event
                text = driver.execute_script("return arguments[0].innerText;", number_event[i])
                pattern = re.compile(r'\[(\d+)\]')

                # Пошук у тексті за допомогою регулярного виразу
                match = pattern.search(text)

                # -----------------------------#

                try:
                    """ Блок зміни ціни"""
                    try:
                        event = Event.objects.get(announcement_number=int(listing_id))
                        if event.price != price:
                            event.ticket_quantity = ticket_quantity
                            event.price=price
                            event.bot=bot
                            event.save()
                            telegram_bot = telebot.TeleBot(settings.token)
                            chat_id = int(settings.chat_id)
                            message_text = f"Event: {event.event}\n" \
                                            f"Data: {event.data_time}\n" \
                                            f"Location: {event.location}\n" \
                                            f"Ticket Quantity: {event.ticket_quantity}\n" \
                                            f"Price: {event.price}"
                            telegram_bot.send_message(chat_id, message_text)

                    # ------------------------------------- #
                    except ObjectDoesNotExist:
                        Event.objects.create(event=name_event[i].text.replace(number_event[i].text, '').strip(),
                                                 data_time=datetime.strptime(data_time[i].text, "%a %b %d %Y %H:%M").replace(tzinfo=timezone.utc),
                                                 location=location[i].text,
                                                 number_event=int(match.group(1)),
                                                 announcement_number=int(listing_id),
                                                 sector=sector,
                                                 ticket_quantity=ticket_quantity,
                                                 features=str(features_list),
                                                 state=str(state_check_box),
                                                 net_price=net_price,
                                                 price=price,
                                                 bot=bot)

                except selenium.common.exceptions.StaleElementReferenceException as e:
                    print(e)
                    print('-----------------------------------')
                    continue

            driver.execute_script("arguments[0].click();", elements[i])

        # Закриття браузер
        driver.quit()