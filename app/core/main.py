import flet as ft
import subprocess
import psutil
import pystray
from PIL import Image

__alt_path = r'assets/scripts/spotyCompiler/Spotify/bin/Debug/net9.0/AltSpotify.exe'
__shift_path = r'assets/scripts/spotyCompiler/ShiftSpotify/bin/Debug/net9.0/ShiftSpotify.exe'
__icon_path = r'assets/icon.png'

tray_icon = Image.open(__icon_path)
p: ft.Page


def kill_process_by_name(process_name):
    """Завершает процесс по имени."""
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                proc.kill()
                print(f"Процесс {process_name} завершен.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def exit_app(icon, query):
    button_clicked(None)
    icon.stop()
    kill_process_by_name("ShiftSpotify.exe")
    kill_process_by_name("AltSpotify.exe")
    p.window.destroy()


def start_shift_script(e):
    kill_process_by_name("ShiftSpotify.exe")
    try:
        kill_process_by_name("AltSpotify.exe")
        subprocess.run(__shift_path, check=True)
    except Exception as e:
        print(f"Ошибка при запуске Shift скрипта: {e}")


def start_alt_script(e):
    kill_process_by_name("AltSpotify.exe")
    try:
        kill_process_by_name("ShiftSpotify.exe")
        subprocess.run(__alt_path, check=True)
    except Exception as e:
        print(f"Ошибка при запуске Alt скрипта: {e}")


def other_item_clicked(icon, query):
    button_clicked(None)
    print("A Non-Default button was pressed.")


def default_item_clicked(icon, query):
    button_clicked(None)
    icon.visible = False
    p.window.skip_task_bar = False
    p.window.maximized = False
    p.update()


def menu_item_clicked(icon, query):
    button_clicked(None)

    if str(query) == "Open App":
        icon.visible = False
        p.window_skip_task_bar = False
        p.window_maximized = False
        p.update()
    elif str(query) == "Close App":
        icon.stop()
        p.window_close()
    else:
        print("A Non-Default button was pressed.")


def my_setup(icon):
    icon.visible = False


tray_icon = pystray.Icon(
    name="SpotifyController",
    icon=tray_icon,
    title="SpotifyController",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Open App",
            default_item_clicked,
            default=True
        ),
        pystray.MenuItem(
            "Alt",
            start_alt_script,
        ),
        pystray.MenuItem(
            "Shift",
            start_alt_script
        ),
        pystray.MenuItem(
            "Close App",
            exit_app
        )
    ),
    visible=False,
)


def on_window_event(e):
    if e.data == "minimize":
        tray_icon.visible = True
        p.window.skip_task_bar = True
    elif e.data == "restore":
        tray_icon.visible = False
        p.window.skip_task_bar = False
    elif e.data == "close":
        tray_icon.stop()
        e.page.window.destroy()
        kill_process_by_name("ShiftSpotify.exe")
        kill_process_by_name("AltSpotify.exe")
    p.update()


def button_clicked(e):
    print("non default button pressed")


def main(page: ft.Page):
    global p
    p = page

    page.title = "SpotifyScript"
    page.window.resizable = False
    page.window.center()
    page.window.height = 500
    page.window.width = 400
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1b1c1e"
    page.window.on_event = on_window_event
    page.window.prevent_close = True

    page.fonts = {
        "Montserrat": "https://fonts.google.com/share?selection.family=Montserrat:ital,wght@0,100..900;1,100..900"
    }

    def contact_with_me_alert(e):
        page.overlay.append(dlg_contacts)
        dlg_contacts.open = True
        page.update()

    def close_dialog(e):
        dlg_contacts.open = False
        page.update()

    def on_click_outside_dialog(e):
        if dlg_contacts.open:
            close_dialog(e)

    def switch_hover_button_color_shift(e):
        if e.data == "true":
            shiftButton.bgcolor = "#21db56"
        else:
            shiftButton.bgcolor = "#27502c"
        page.update()

    def switch_hover_button_color_alt(e):
        if e.data == "true":
            altButton.bgcolor = "#21db56"
        else:
            altButton.bgcolor = "#27502c"
        page.update()

    def switch_hover_button_color_contact(e):
        if e.data == "true":
            messageButton.bgcolor = "#f55959"
        else:
            messageButton.bgcolor = "#902d2a"
        page.update()

    dlg_contacts = ft.AlertDialog(
        modal=True,
        title=ft.Text("Contact with me"),
        content=ft.Column(
            [
                ft.Text("TG - @qxzxbtlqq"),
                ft.Text("VK - xxzxbtl"),
                ft.Text("GitHub - xzxbtl")
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton("Close", on_click=close_dialog)
        ]
    )

    main_text = ft.Container(
        ft.Column(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Choose Script Combination",
                            size=25,
                            font_family="Montserrat",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        )
                    ],
                ),
                ft.Divider(height=8)
            ]
        ),
        padding=ft.Padding(left=20, top=60, right=20, bottom=20)
    )

    shiftButton = ft.ElevatedButton(
        "Shift",
        color="#ffffff",
        bgcolor="#27502c",
        on_click=start_shift_script,
        width=100,
        on_hover=switch_hover_button_color_shift,
    )
    altButton = ft.ElevatedButton(
        "Alt",
        color="#ffffff",
        bgcolor="#27502c",
        on_click=start_alt_script,
        width=100,
        on_hover=switch_hover_button_color_alt,
    )

    messageButton = ft.ElevatedButton(
        "Contact Me",
        color="#ffffff",
        bgcolor="#902d2a",
        on_click=contact_with_me_alert,
        width=100,
        on_hover=switch_hover_button_color_contact,
    )

    main_buttons = ft.Container(
        ft.Column(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        shiftButton,
                        altButton
                    ],
                    spacing=60
                )
            ]
        ),
        padding=ft.Padding(left=20, top=10, right=20, bottom=20)
    )

    contact_me_container = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        messageButton,
                    ],
                ),
            ],
        ),
        padding=ft.Padding(left=20, top=10, right=20, bottom=20)
    )

    page.add(main_text, main_buttons, contact_me_container, dlg_contacts)
    page.update()


if __name__ == "__main__":
    tray_icon.run_detached(setup=my_setup)
    ft.app(target=main)
