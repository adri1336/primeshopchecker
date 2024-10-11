from selenium.webdriver.common.by import By


def GAME_check_product_stock(browser):
    url = browser.current_url
    if "game.es" not in url:
        return {"message": "ERROR", "buy_button": None}

    try:
        browser.find_element(By.ID, "body")
    except:
        return {"message": "ERROR", "buy_button": None}

    try:
        buy_button = browser.find_element(By.ID, "btnNEW")
        return {"message": "STOCK", "buy_button": buy_button}
    except:
        return {"message": "OUT_OF_STOCK", "buy_button": None}
