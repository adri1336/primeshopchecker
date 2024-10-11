import flet as ft


def about_view(go_home, launch_url):
    return ft.View(
        "/about",
        padding=20,
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton("Volver", on_click=lambda _: go_home()),
                    ft.Text("Acerca de PrimeShopChecker",
                            size=20, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Versión: 1.0.0"),
                    ft.Text("Hecho por: adri1 (adri1pawn@gmail.com)"),
                    ft.Row([
                        ft.TextButton("Comprobar actualizaciones", on_click=lambda _: launch_url(
                            "https://github.com/adri1336/primeshopchecker/releases")),
                        ft.TextButton("Ver código fuente", on_click=lambda _: launch_url(
                            "https://github.com/adri1336/primeshopchecker")),
                    ], spacing=50)
                ]),
                padding=20,
            )
        ]
    )
