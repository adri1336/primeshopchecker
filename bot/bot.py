import threading
from bot.shops.playstation import PLAYSTATION_check_product_stock
from bot.shops.mediamarkt import MEDIAMARKT_check_product_stock
from bot.shops.game import GAME_check_product_stock
from bot.shops.fnac import FNAC_check_product_stock
from bot.shops.amazon import AMAZON_check_product_stock
from bot.shops.carrefour import CARREFOUR_check_product_stock
from bot.shops.eci import ECI_check_product_stock
import undetected_chromedriver as uc
import pyautogui
import random
import time
import requests


class BotManager:
    def __init__(self):
        self.settings = None
        self.products = None
        self.update_home = None
        self.write_products = None
        self.stock_timer = None
        self.stock_browser = None
        self.proxy_timer = None
        self.launch_url = None
        self.reset_on_next = False
        self.play_stock_sound = None
        self.stop_event = threading.Event()

    def init_stock_browser(self):
        if self.stock_browser is not None:
            self.stock_browser.quit()
            self.stock_browser = None

        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")

        if len(self.settings["user_agents"]) > 0:
            user_agent = random.choice(self.settings["user_agents"])
            print(f"Using user agent: {user_agent}")
            options.add_argument(f'user-agent={user_agent}')

        if self.settings["headless"] and not self.settings["use_proxy"]:
            options.add_argument("--headless")

        if self.settings["use_proxy"]:
            options.add_argument(
                f'--proxy-server={self.settings["proxy"]["host"]}')

        self.stock_browser = uc.Chrome(options=options)
        self.stock_browser.set_page_load_timeout(30)  # 30 seconds

        if self.settings["use_proxy"]:
            # login to proxy
            self.stock_browser.get("https://ipchicken.com/")
            time.sleep(0.5)
            pyautogui.typewrite(self.settings["proxy"]["user"])
            pyautogui.press('tab')
            pyautogui.typewrite(self.settings["proxy"]["pass"])
            pyautogui.press('enter')

        self.start_stock_timer()

    def reset_stock_browser(self):
        print("Resetting browser")
        if self.stock_timer is not None:
            self.stock_timer.cancel()
            self.stock_timer = None

        if self.proxy_timer is not None:
            self.proxy_timer.cancel()
            self.proxy_timer = None

        if self.stock_browser is not None:
            self.stock_browser.quit()
            self.stock_browser = None

        time.sleep(1)
        threading.Thread(target=self.init_stock_browser).start()

    def update_bot_settings(self, new_settings):
        self.settings = new_settings
        if self.stock_browser is not None:
            self.reset_on_next = True

    def update_bot_products(self, new_products):
        self.products = new_products
        if self.stock_browser is not None:
            self.reset_on_next = True

    def load_main_bot(self, update_home, write_products, launch_url, play_stock_sound):
        self.update_home = update_home
        self.write_products = write_products
        self.launch_url = launch_url
        self.play_stock_sound = play_stock_sound
        if self.settings is not None:
            threading.Thread(target=self.init_stock_browser).start()

    def get_stock_browser_window(self, url):
        for window in self.stock_browser.window_handles:
            self.stock_browser.switch_to.window(window)
            if url == self.stock_browser.current_url:
                return window

        return None

    def launch_notification(self, product):
        pushover_token = self.settings["pushover_token"]
        pushover_user = self.settings["pushover_user"]

        if len(pushover_token) > 0 and len(pushover_user) > 0:
            print(f"Sending notification for {pushover_token} {pushover_user}")
            requests.post("https://api.pushover.net/1/messages.json", data={
                "token": pushover_token,
                "user": pushover_user,
                "message": f"{product['name']} disponible",
                "url": product["url"]
            })

    def check_stock(self):
        if self.reset_on_next:
            self.reset_on_next = False
            self.reset_stock_browser()
            return

        if self.stock_browser is None:
            return

        for index, product in enumerate(self.products):
            if self.stop_event.is_set():
                break

            if product["active"] is False or product["state"] == "STOCK":
                continue

            self.products[index]["state"] = "CHECKING"
            self.write_products(self.products)
            self.update_home()

            try:
                window = self.get_stock_browser_window(product["url"])
                if window is not None:
                    self.stock_browser.switch_to.window(window)
                    self.stock_browser.refresh()
                else:
                    self.stock_browser.execute_script("window.open();")
                    self.stock_browser.switch_to.window(
                        self.stock_browser.window_handles[-1])
                    self.stock_browser.get(product["url"])

                new_state = {"message": "ERROR", "buy_button": None}

                if "direct.playstation.com" in product["url"]:
                    new_state = PLAYSTATION_check_product_stock(
                        self.stock_browser)
                elif "mediamarkt.es" in product["url"]:
                    new_state = MEDIAMARKT_check_product_stock(
                        self.stock_browser)
                elif "game.es" in product["url"]:
                    new_state = GAME_check_product_stock(
                        self.stock_browser)
                elif "fnac.es" in product["url"]:
                    new_state = FNAC_check_product_stock(
                        self.stock_browser)
                elif "amazon.es" in product["url"] or "amzn.eu" in product["url"]:
                    new_state = AMAZON_check_product_stock(
                        self.stock_browser)
                elif "carrefour.es" in product["url"]:
                    new_state = CARREFOUR_check_product_stock(
                        self.stock_browser)
                elif "elcorteingles.es" in product["url"]:
                    new_state = ECI_check_product_stock(
                        self.stock_browser)

                if new_state["message"] == "STOCK":
                    threading.Thread(target=self.play_stock_sound).start()
                    self.stock_browser.close()

                    if self.products[index]["notice_when_available"]:
                        self.launch_url(self.products[index]["url"])
                        self.launch_notification(self.products[index])

                self.products[index]["state"] = new_state["message"]
            except:
                self.products[index]["state"] = "ERROR"
            finally:
                if self.stop_event.is_set():
                    return
                self.write_products(self.products)
                self.update_home()

        if int(self.settings["check_stock_interval"]) > 0:
            self.stock_timer = threading.Timer(
                int(self.settings["check_stock_interval"]), self.check_stock)
            self.stock_timer.start()
        else:
            self.stock_timer = None
            self.check_stock()

    def reset_stock_browser_on_next(self):
        print("Resetting browser on next check for change proxy")
        self.reset_on_next = True

    def kill(self):
        self.stop_event.set()
        if self.stock_timer is not None:
            self.stock_timer.cancel()
            self.stock_timer = None

        if self.proxy_timer is not None:
            self.proxy_timer.cancel()
            self.proxy_timer = None

        if self.stock_browser is not None:
            self.stock_browser.quit()
            self.stock_browser = None

    def start_stock_timer(self):
        if self.stock_timer is not None:
            self.stock_timer.cancel()
            self.stock_timer = None

        threading.Thread(target=self.check_stock).start()

        if self.proxy_timer is not None:
            self.proxy_timer.cancel()
            self.proxy_timer = None

        if self.settings["use_proxy"]:
            minutes = float(self.settings["proxy"]["time_minutes"])
            self.proxy_timer = threading.Timer(
                minutes * 60, self.reset_stock_browser_on_next)
            self.proxy_timer.start()
