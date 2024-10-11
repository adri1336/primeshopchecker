import flet as ft


def add_view(go_home, load_products, write_products):
    new_product = {
        "id": 0,
        "name": "",
        "url": "",
        "state": "LOADING",
        "notice_when_available": True,
        "active": True,
    }

    def on_click_add():
        products = load_products()
        if len(products) == 0:
            new_product["id"] = 1
        else:
            new_product["id"] = max([product["id"]
                                    for product in products]) + 1

        products.append(new_product)
        write_products(products, True)

    def on_textfield_change(e, key):
        new_product[key] = e.control.value

    def on_switch_change(e, key):
        new_product[key] = e.control.value

    return ft.View(
        "/add",
        padding=20,
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton("Volver", on_click=lambda _: go_home()),
                    ft.Text("Añadir producto", size=20, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Column([
                        ft.Text("Nombre"),
                        ft.TextField(
                            value=new_product["name"],
                            border_color=ft.colors.BLUE_100,
                            on_change=lambda e: on_textfield_change(e, "name")
                        )
                    ]),
                    ft.Column([
                        ft.Text("URL"),
                        ft.TextField(
                            value=new_product["url"],
                            border_color=ft.colors.BLUE_100,
                            on_change=lambda e: on_textfield_change(e, "url")
                        )
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Text("Avisar cuando esté disponible"),
                            ft.Switch(
                                value=new_product["notice_when_available"],
                                on_change=lambda e: on_switch_change(
                                    e, "notice_when_available")
                            )
                        ], expand=True),
                        ft.Column([
                            ft.Text("Activo"),
                            ft.Switch(
                                value=new_product["active"],
                                on_change=lambda e: on_switch_change(
                                    e, "active")
                            )
                        ], expand=True),
                    ]),
                ]),
                alignment=ft.alignment.center,
                margin=20,
                expand=True,
            ),
            ft.Row(
                controls=[
                    ft.FilledButton(
                        "Añadir", on_click=lambda _: on_click_add()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.alignment.center,
            ),
        ]
    )
