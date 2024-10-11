from selenium.webdriver.common.by import By


def MEDIAMARKT_check_product_stock(browser):
    url = browser.current_url
    if "mediamarkt.es" not in url:
        return {"message": "ERROR", "buy_button": None}

    try:
        browser.find_element(By.ID, "root")
    except:
        return {"message": "ERROR", "buy_button": None}

    try:
        buy_button = browser.find_element(By.ID, "pdp-add-to-cart-button")
        return {"message": "STOCK", "buy_button": buy_button}
    except:
        return {"message": "OUT_OF_STOCK", "buy_button": None}
