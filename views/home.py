import flet as ft


def home_view(page: ft.Page, last_updated: ft.Text, load_products, select_product, go_settings, go_add, go_about, reset_stock_browser):
    products = load_products()

    def on_url_click(product):
        page.launch_url(product["url"])

    def create_row(product):
        return ft.DataRow(cells=[
            ft.DataCell(ft.Text(product["name"],
                        size=14, width=100, no_wrap=True)),
            ft.DataCell(
                ft.CupertinoButton(
                    content=ft.Text(
                        product["url"], color=ft.colors.BLUE_100, size=14, no_wrap=True),
                    width=300,
                    alignment=ft.alignment.top_left,
                    on_click=lambda e, p=product: on_url_click(p)
                )
            ),
            ft.DataCell(ft.Text(product["state"])),
            ft.DataCell(
                ft.Text("Sí" if product["notice_when_available"] else "No")),
            ft.DataCell(ft.Text("Sí" if product["active"] else "No")),
            ft.DataCell(ft.TextButton("Editar", on_click=lambda e,
                        p=product: select_product(p))),
        ])

    def reset_stock_browser_button():
        reset_stock_browser()

    return ft.View(
        "/home",
        padding=20,
        controls=[
            ft.Row(
                [
                    ft.Row([
                        ft.Text("PrimeShopChecker", size=24, weight="bold"),
                        ft.IconButton(
                            ft.icons.INFO_OUTLINED, on_click=lambda _: go_about()),
                    ]),
                    ft.TextButton("Añadir", on_click=lambda _: go_add())
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Producto")),
                        ft.DataColumn(ft.Text("URL")),
                        ft.DataColumn(ft.Text("Estado")),
                        ft.DataColumn(
                            ft.Text("Avisar cuando haya stock (S/N)")),
                        ft.DataColumn(ft.Text("Activo")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=[create_row(product) for product in products],
                    width=99999
                ),
                alignment=ft.alignment.top_left,
                expand=True,
            ),
            ft.Row(
                [
                    ft.TextButton("Reiniciar navegador",
                                  on_click=lambda _: reset_stock_browser_button()),
                    last_updated,
                    ft.TextButton("Ajustes", on_click=lambda _: go_settings())
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        ]
    )
