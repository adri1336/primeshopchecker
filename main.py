import flet as ft
from views.home import home_view
from views.edit import edit_view
from views.settings import settings_view
from views.add import add_view
from views.about import about_view
from datetime import datetime
from bot.bot import BotManager
import threading
import json
from playsound import playsound


def main(page: ft.Page):
    selected_product = None
    last_updated = ft.Text("Iniciando...", size=14)
    settings = None
    products = None
    banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        content=ft.Text(
            value="",
            color=ft.colors.BLACK,
            weight="bold",
        ),
        actions=[
            ft.TextButton(text="Cerrar", on_click=lambda e: close_banner())
        ],
    )
    bot_manager = BotManager()

    def open_banner(time=3):
        page.open(banner)
        if time > 0:
            threading.Timer(time, close_banner).start()

    def close_banner():
        page.close(banner)

    def write_settings(new_settings, message=False):
        nonlocal settings
        settings = new_settings
        with open('data/settings.json', 'w', encoding='utf-8') as file:
            json.dump(settings, file, indent=4)

        if message:
            bot_manager.update_bot_settings(settings)
            banner.content.value = "Configuración guardada correctamente"
            banner.bgcolor = ft.colors.GREEN_100
            banner.leading = ft.Icon(
                ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=30)
            open_banner()

    def load_settings():
        nonlocal settings
        try:
            with open('data/settings.json', 'r', encoding='utf-8') as file:
                settings = json.load(file)
        except:
            settings = {
                "headless": True,
                "check_stock_interval": "10",
                "use_proxy": False,
                "proxy": {
                    "host": "",
                    "user": "",
                    "pass": "",
                    "time_minutes": "20"
                },
                "pushover_token": "",
                "pushover_user": "",
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
                ],
            }
            write_settings(settings)
        finally:
            return settings

    def write_products(new_products, message=False):
        nonlocal products
        products = new_products
        with open('data/products.json', 'w', encoding='utf-8') as file:
            json.dump(products, file, indent=4)

        if message:
            bot_manager.update_bot_products(products)
            banner.content.value = "Productos actualizados correctamente"
            banner.bgcolor = ft.colors.GREEN_100
            banner.leading = ft.Icon(
                ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=30)
            open_banner()

    def load_products(first_time=False):
        nonlocal products
        try:
            with open('data/products.json', 'r', encoding='utf-8') as file:
                products = json.load(file)
        except:
            products = []
            write_products(products)
        finally:
            if first_time:
                for i in range(len(products)):
                    if products[i]["state"] != "STOCK":
                        if products[i]["active"] is False:
                            products[i]["state"] = "INACTIVE"
                        else:
                            products[i]["state"] = "LOADING"
            return products

    def current_page():
        return page.views[0].route

    def reset_stock_browser():
        bot_manager.reset_stock_browser()

    def go_about():
        page.views.clear()
        page.views.append(
            about_view(go_home, launch_url))
        page.update()

    def go_home():
        page.views.clear()
        page.views.append(
            home_view(page, last_updated, load_products, select_product, go_settings, go_add, go_about, reset_stock_browser))
        page.update()

    def go_add():
        page.views.clear()
        page.views.append(add_view(
            go_home, load_products, write_products))
        page.update()

    def go_settings():
        page.views.clear()
        page.views.append(settings_view(
            go_home, load_settings, write_settings))
        page.update()

    def select_product(product):
        nonlocal selected_product
        selected_product = product
        page.views.clear()
        page.views.append(edit_view(go_home, selected_product,
                          load_products, write_products))
        page.update()

    def update_home():
        last_updated.value = f"Última actualización: {
            datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}"
        if current_page() == "/home":
            go_home()

    def launch_url(url):
        page.launch_url(url)

    def play_stock_sound():
        playsound("data/bell.mp3")

    def handle_window_event(e):
        if e.data == "close":
            bot_manager.kill()
            page.window.destroy()

    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    load_settings()
    load_products(True)
    bot_manager.update_bot_settings(settings)
    bot_manager.update_bot_products(products)
    bot_manager.load_main_bot(
        update_home, write_products, launch_url, play_stock_sound)
    go_home()


ft.app(target=main)
