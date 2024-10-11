import flet as ft


def edit_view(go_home, selected_product, load_products, write_products):
    products = load_products()
    reset_if_stock = ft.Row([])

    def stock_reset():
        reset_if_stock.controls = [
            ft.Row([
                ft.Text("")
            ], spacing=20)
        ]
        for i, product in enumerate(products):
            if product["id"] == selected_product["id"]:
                products[i]["state"] = "LOADING"
                break

        reset_if_stock.update()
        write_products(products, True)
        pass

    if selected_product["state"] == "STOCK":
        reset_if_stock.controls = [
            ft.Row([
                ft.Column([
                    ft.TextButton("Comprobar de nuevo",
                                  on_click=lambda _: stock_reset()),
                ]),
            ], spacing=20)
        ]

    def on_click_save():
        for i, product in enumerate(products):
            if product["id"] == selected_product["id"]:
                products[i] = selected_product
                if products[i]["state"] != "STOCK":
                    if products[i]["active"] is False:
                        products[i]["state"] = "INACTIVE"
                    else:
                        products[i]["state"] = "LOADING"
                break
        write_products(products, True)

    def on_click_delete():
        for i, product in enumerate(products):
            if product["id"] == selected_product["id"]:
                products.pop(i)
                break
        write_products(products, True)
        go_home()

    def on_textfield_change(e, key):
        selected_product[key] = e.control.value

    def on_switch_change(e, key):
        selected_product[key] = e.control.value

    return ft.View(
        "/edit",
        padding=20,
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton("Volver", on_click=lambda _: go_home()),
                    ft.Text("Editar producto", size=20, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Column([
                        ft.Text("Nombre"),
                        ft.TextField(
                            value=selected_product["name"],
                            border_color=ft.colors.BLUE_100,
                            on_change=lambda e: on_textfield_change(e, "name")
                        )
                    ]),
                    ft.Column([
                        ft.Text("URL"),
                        ft.TextField(
                            value=selected_product["url"],
                            border_color=ft.colors.BLUE_100,
                            on_change=lambda e: on_textfield_change(e, "url")
                        )
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Text("Avisar cuando esté disponible"),
                            ft.Switch(
                                value=selected_product["notice_when_available"],
                                on_change=lambda e: on_switch_change(
                                    e, "notice_when_available")
                            )
                        ], expand=True),
                        ft.Column([
                            ft.Text("Activo"),
                            ft.Switch(
                                value=selected_product["active"],
                                on_change=lambda e: on_switch_change(
                                    e, "active")
                            )
                        ], expand=True),
                    ])
                ]),
                alignment=ft.alignment.center,
                margin=20,
                expand=True,
            ),
            ft.Row(
                controls=[
                    reset_if_stock,
                    ft.FilledButton(
                        "Guardar", on_click=lambda _: on_click_save()),
                    ft.TextButton(
                        text="Eliminar", on_click=lambda _: on_click_delete()),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.alignment.center,
            ),
        ]
    )
