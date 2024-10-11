import flet as ft


def settings_view(go_home, load_settings, write_settings):
    settings = load_settings()

    # Contenedor de los controles del proxy
    proxy_controls_container = ft.Column([])

    def on_click_save():
        write_settings(settings, True)

    def on_textfield_change(e, key, subkey=None):
        # Actualiza el valor en settings
        if subkey:
            settings[key][subkey] = e.control.value
        else:
            settings[key] = e.control.value

    def on_switch_proxy_change(e):
        # Actualiza la configuración de proxy en settings
        settings["use_proxy"] = e.control.value
        # Actualiza los controles del proxy según el estado del switch
        proxy_controls_container.controls = [
            ft.Row([
                ft.Column([
                    ft.Text("Usar proxy"),
                    ft.Switch(
                        value=settings["use_proxy"],
                        on_change=on_switch_proxy_change
                    )
                ]),
                ft.Column([
                    ft.Text("Host"),
                    ft.TextField(
                        value=settings["proxy"]["host"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "host")
                    )
                ], expand=True)
            ], spacing=20),
            ft.Row([
                ft.Column([
                    ft.Text("Usuario"),
                    ft.TextField(
                        value=settings["proxy"]["user"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "user")
                    )
                ], expand=True),
                ft.Column([
                    ft.Text("Contraseña"),
                    ft.TextField(
                        value=settings["proxy"]["pass"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "pass")
                    )
                ], expand=True),
                ft.Column([
                    ft.Text("Cambio de IP (minutos)"),
                    ft.TextField(
                        value=settings["proxy"]["time_minutes"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "time_minutes")
                    )
                ], expand=True),
            ])
        ] if settings["use_proxy"] else [
            ft.Column([
                ft.Text("Usar proxy"),
                ft.Switch(
                    value=settings["use_proxy"],
                    on_change=on_switch_proxy_change
                )
            ])
        ]

        # Actualiza la vista para reflejar los cambios
        proxy_controls_container.update()

    # Inicializa los controles del proxy si 'use_proxy' es True
    if settings["use_proxy"]:
        proxy_controls_container.controls = [
            ft.Row([
                ft.Column([
                    ft.Text("Usar proxy"),
                    ft.Switch(
                        value=settings["use_proxy"],
                        on_change=on_switch_proxy_change
                    )
                ]),
                ft.Column([
                    ft.Text("Host"),
                    ft.TextField(
                        value=settings["proxy"]["host"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "host")
                    )
                ], expand=True)
            ], spacing=20),
            ft.Row([
                ft.Column([
                    ft.Text("Usuario"),
                    ft.TextField(
                        value=settings["proxy"]["user"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "user")
                    )
                ], expand=True),
                ft.Column([
                    ft.Text("Contraseña"),
                    ft.TextField(
                        value=settings["proxy"]["pass"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "pass")
                    )
                ], expand=True),
                ft.Column([
                    ft.Text("Cambio de IP (minutos)"),
                    ft.TextField(
                        value=settings["proxy"]["time_minutes"],
                        border_color=ft.colors.BLUE_100,
                        on_change=lambda e: on_textfield_change(
                            e, "proxy", "time_minutes")
                    )
                ], expand=True),
            ])
        ]
    else:
        proxy_controls_container.controls = [
            ft.Column([
                ft.Text("Usar proxy"),
                ft.Switch(
                    value=settings["use_proxy"],
                    on_change=on_switch_proxy_change
                )
            ])
        ]

    return ft.View(
        "/settings",
        padding=20,
        auto_scroll=True,
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton("Volver", on_click=lambda _: go_home()),
                    ft.Text("Ajustes", size=20, weight="bold"),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text("Modo silencioso"),
                            ft.Switch(
                                value=settings["headless"],
                                on_change=lambda e: on_textfield_change(
                                    e, "headless")
                            )
                        ]),
                        ft.Column([
                            ft.Text("Intervalo de comprobación (segundos)"),
                            ft.TextField(
                                value=settings["check_stock_interval"],
                                border_color=ft.colors.BLUE_100,
                                on_change=lambda e: on_textfield_change(
                                    e, "check_stock_interval")
                            )
                        ], expand=True),
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Text("Pushover API Token"),
                            ft.TextField(
                                value=settings["pushover_token"],
                                border_color=ft.colors.BLUE_100,
                                on_change=lambda e: on_textfield_change(
                                    e, "pushover_token")
                            )
                        ], expand=True),
                        ft.Column([
                            ft.Text("Pushover User"),
                            ft.TextField(
                                value=settings["pushover_user"],
                                border_color=ft.colors.BLUE_100,
                                on_change=lambda e: on_textfield_change(
                                    e, "pushover_user")
                            )
                        ], expand=True),
                    ]),
                    proxy_controls_container,
                ], spacing=20),
                alignment=ft.alignment.center,
                margin=20,
                expand=True,
            ),
            ft.Row(
                controls=[
                    ft.FilledButton(
                        "Guardar", on_click=lambda _: on_click_save()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.alignment.center,
            ),
        ]
    )
