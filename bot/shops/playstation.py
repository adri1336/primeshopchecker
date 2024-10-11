from selenium.webdriver.common.by import By
from bot.functions import xpath_find_elements_by_class


def PLAYSTATION_check_product_stock(browser):
    url = browser.current_url
    if "direct.playstation.com" not in url:
        return {"message": "ERROR", "buy_button": None}

    try:
        buy_button = None
        buy_buttons = browser.find_elements(
            By.XPATH, xpath_find_elements_by_class('button', ['btn transparent-orange-button js-login-gated-link', 'btn transparent-orange-button js-analyitics-tag add-to-cart']))
        for button in buy_buttons:
            if button.is_displayed():
                buy_button = button
                break

        if buy_button is None:
            return {"message": "OUT_OF_STOCK", "buy_button": None}
        else:
            return {"message": "STOCK", "buy_button": buy_button}
    except:
        return {"message": "ERROR", "buy_button": None}
