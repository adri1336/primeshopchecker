from selenium.webdriver.common.by import By


def CARREFOUR_check_product_stock(browser):
    url = browser.current_url
    if "carrefour.es" not in url:
        return {"message": "ERROR", "buy_button": None}

    try:
        browser.find_element(By.CLASS_NAME, "product-header")
    except:
        return {"message": "ERROR", "buy_button": None}

    try:
        #
        buy_button = browser.find_element(
            By.CLASS_NAME, "add-to-cart-button__full-button.add-to-cart-button__button")
        return {"message": "STOCK", "buy_button": buy_button}
    except:
        return {"message": "OUT_OF_STOCK", "buy_button": None}
