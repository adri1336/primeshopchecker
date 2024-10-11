from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
from bot.functions import xpath_find_elements_by_text


def AMAZON_direct_buy_button(browser):
    try:
        buy_button = browser.find_element(By.ID, "buy-now-button")
        return buy_button
    except:
        return None


def AMAZON_check_product_stock(browser):
    url = browser.current_url
    # a-row a-text-center
    if "amazon.es" in url or "amzn.eu" in url:
        captcha_src = None
        try:
            # a-row a-text-center
            captcha_src = browser.find_element(
                By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute("src")
        except:
            pass

        if captcha_src is not None:
            captcha = AmazonCaptcha.fromlink(captcha_src)
            captcha_value = AmazonCaptcha.solve(captcha)

            input_captcha = browser.find_element(By.ID, "captchacharacters")
            input_captcha.send_keys(captcha_value)

            button = browser.find_element(By.CLASS_NAME, "a-button-text")
            button.click()

        try:
            browser.find_element(By.ID, "ap_container")
        except:
            return {"message": "ERROR", "buy_button": None}

        try:
            browser.find_element(
                By.XPATH, xpath_find_elements_by_text('span', ['No disponible.']))
            return {"message": "OUT_OF_STOCK", "buy_button": None}
        except:
            pass

        return {"message": "STOCK", "buy_button": None}

    else:
        return {"message": "ERROR", "buy_button": None}
