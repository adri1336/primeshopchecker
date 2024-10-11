from selenium.webdriver.common.by import By
from bot.functions import xpath_find_elements_by_text


def FNAC_check_product_stock(browser):
    url = browser.current_url
    if "fnac.es" not in url:
        return {"message": "ERROR", "buy_button": None}

    try:
        # find by class
        browser.find_element(By.CLASS_NAME, "f-productHeader")
    except:
        return {"message": "ERROR", "buy_button": None}

    try:
        #
        buy_button = browser.find_element(
            By.XPATH, xpath_find_elements_by_text('span', ['Comprar en un clic']))
        return {"message": "STOCK", "buy_button": buy_button}
    except:
        return {"message": "OUT_OF_STOCK", "buy_button": None}
