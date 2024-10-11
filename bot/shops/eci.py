from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot.functions import xpath_find_elements_by_text


def ECI_check_product_stock(browser):
    url = browser.current_url
    if "elcorteingles.es" not in url:
        return {"message": "ERROR", "buy_button": None}

    # get page title
    title = browser.title
    if title == "Challenge Validation":
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "product_detail__container"))
        )

    try:
        browser.find_element(By.CLASS_NAME, "product_detail__container")
    except:
        return {"message": "ERROR", "buy_button": None}

    try:
        buy_button = None
        buy_buttons = browser.find_elements(
            By.XPATH, xpath_find_elements_by_text('button', ['cesta']))

        for button in buy_buttons:
            if button.is_displayed():
                buy_button = button
                break

        if buy_button is not None:
            return {"message": "STOCK", "buy_button": buy_button}
        else:
            return {"message": "OUT_OF_STOCK", "buy_button": None}
    except:
        return {"message": "OUT_OF_STOCK", "buy_button": None}
