
import os
import sys
import traceback
import subprocess
import psutil
import ctypes
import winreg
import tkinter as tk
from tkinter import messagebox

# ============================================================
# PATHS
# ============================================================

APP_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

INDEX = os.path.join(APP_DIR, "Index.html")
CONFIG = os.path.join(APP_DIR, "debug.cfg")

# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {
    "Show Console": False,
    "ConsoleStays": True,
    "Initializehutdowns": True,
    "UseSteamUrls": False,
    "SteamDesktopConsole": False
}


def load_config():
    if not os.path.exists(CONFIG):
        default_text = """
## Python stuff:

# Show the Python console while starting
Show Console: false

# Press enter to close console
ConsoleStays: true

## Boot Select:

# Allow actual Windows power commands (Shutdown, Restart, Log Off)
Initializehutdowns: true

# Use Steam URLs instead of checking the registry (ex. steam://open/bigpicture)
UseSteamUrls: false


# Allows to launch Steam in desktop mode (with console). Unnessesary setting.
SteamDesktopConsole: false

"""

        with open(CONFIG, "w", encoding="utf-8") as file:
            file.write(default_text)

    settings = DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith(("#", ";")) or ":" not in line:
                    continue

                key, value = line.split(":", 1)

                key = key.strip()
                value = value.strip().lower()

                if key in settings and value in ("true", "false"):
                    settings[key] = value == "true"

    except Exception as error:
        print("[CONFIG] Failed to read debug.cfg:", error)

    return settings


settings = load_config()

SHOW_CONSOLE = settings["Show Console"]
CONSOLE_STAYS = settings["ConsoleStays"]
INITIALIZE_SHUTDOWNS = settings["Initializehutdowns"]
USE_STEAM_URLS = settings["UseSteamUrls"]
STEAM_DESKTOP_CONSOLE = settings["SteamDesktopConsole"]


# ============================================================
# LOGON CHANGER
# ============================================================

HOST_EXE = os.path.join(APP_DIR, "Host.exe")
REG_PATH = r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon"

def run_logon_changer():

    def set_shell(value):
        try:
            with winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER,
                REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(
                    key, "Shell", 0, winreg.REG_SZ, value
                )
            return True

        except OSError as error:
            messagebox.showerror(
                "Registry Error",
                f"Could not modify the registry:\n\n{error}"
            )
            return False

    def get_shell():
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REG_PATH,
                0,
                winreg.KEY_READ
            ) as key:
                return winreg.QueryValueEx(key, "Shell")[0]

        except FileNotFoundError:
            return "explorer.exe"
        except OSError:
            return "Unknown"
    
    def update_status():
        current = get_shell()
    
        if current.lower() == "explorer.exe":
            status_label.config(
                text="Current shell: Windows Explorer",
                fg="#75c98b"
            )
        elif current.lower() == f'"{HOST_EXE}"'.lower():
            status_label.config(
                text="Current shell: Host.exe",
                fg="#75a9e8"
            )
        else:
            status_label.config(
                text="Current shell: Custom / Unknown",
                fg="#d6aa69"
            )
    
        shell_value_label.config(
            text=f"Registry value: {current}"
        )

    def set_as_logon():
        if not os.path.isfile(HOST_EXE):
            messagebox.showerror(
                "Host.exe Not Found",
                f"Could not find Host.exe:\n\n{HOST_EXE}"
            )
            return

        if not messagebox.askyesno(
            "Set Host.exe as Logon",
            "Are you sure you want to replace Explorer with Host.exe?\n\n"
            "WARNING:\n"
            "Windows will launch Host.exe instead of explorer.exe "
            "when you log in.\n\n"
            "If Host.exe fails to start or you cannot launch Explorer, "
            "you may get stuck without your normal desktop and taskbar.\n\n"
            "Make sure you have a recovery method before continuing."
        ):
            return

        if set_shell(f'"{HOST_EXE}"'):
            messagebox.showinfo(
                "Success",
                "Boot Select has been configured as your logon shell.\n\n"
                "The change takes effect after your next sign-in."
            )
            update_status()

    def restore_explorer():
        if not messagebox.askyesno(
            "Restore Explorer",
            "Are you sure you want to restore Windows Explorer "
            "as your logon shell?"
        ):
            return

        if set_shell("explorer.exe"):
            messagebox.showinfo(
                "Success",
                "Windows Explorer has been restored.\n\n"
                "The change takes effect after your next sign-in."
            )
            update_status()

    def open_app_folder():
        os.startfile(APP_DIR)

    root = tk.Tk()
    root.title("Setup (Logon changer)")
    root.geometry("460x380")
    root.resizable(False, False)
    root.configure(bg="#17191e")

    tk.Label(
        root,
        text="Logon changer",
        font=("Segoe UI", 15, "bold"),
        fg="#eeeeee",
        bg="#17191e"
    ).pack(pady=(24, 8))

    tk.Label(
        root,
        text="Configure which application starts at logon.",
        font=("Segoe UI", 9),
        fg="#999da7",
        bg="#17191e"
    ).pack(pady=(0, 20))

    button_style = {
        "font": ("Segoe UI", 10, "bold"),
        "fg": "white",
        "relief": "flat",
        "cursor": "hand2",
        "width": 32,
        "height": 2
    }

    tk.Button(
        root,
        text="Set Boot Select (Host.exe) as Logon",
        bg="#303b50",
        activebackground="#40516d",
        activeforeground="white",
        command=set_as_logon,
        **button_style
    ).pack(pady=5)

    tk.Button(
        root,
        text="Restore Explorer",
        bg="#303030",
        activebackground="#444444",
        activeforeground="white",
        command=restore_explorer,
        **button_style
    ).pack(pady=5)

    status_label = tk.Label(
        root,
        text="",
        font=("Segoe UI", 9),
        bg="#17191e"
    )
    status_label.pack(pady=(15, 0))
    
    shell_value_label = tk.Label(
        root,
        text="",
        font=("Segoe UI", 8),
        fg="#999da7",
        bg="#17191e",
        wraplength=390,
        justify="center"
    )
    shell_value_label.pack(pady=(4, 0))

    tk.Button(
        root,
        text="Open Folder",
        font=("Segoe UI", 8),
        bg="#303030",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=open_app_folder,
        width=12,
        height=1
    ).place(relx=1.0, rely=1.0, x=-12, y=-12, anchor="se")

    update_status()
    root.mainloop()
# Measures if standalone logon changer gets deleted.
#
LOGON_CHANGE_ARGS = {
    "-logonchanger",
    "-logonchange",
    "-logon"
}

if any(arg.lower() in LOGON_CHANGE_ARGS for arg in sys.argv[1:]):
        # Hide console for Logon Changer (it doesn't show anything anyway.)
    try:
        console = ctypes.windll.kernel32.GetConsoleWindow()

        if console:
            ctypes.windll.user32.ShowWindow(console, 0)

    except Exception:
        pass
    run_logon_changer()
    sys.exit(0)
# ============================================================
# CONSOLE
# ============================================================

if not SHOW_CONSOLE:
    try:
        console = ctypes.windll.kernel32.GetConsoleWindow()

        if console:
            ctypes.windll.user32.ShowWindow(console, 0)

    except Exception:
        pass


def wait_for_exit():
    if SHOW_CONSOLE and CONSOLE_STAYS:
        input("\nPress Enter to exit...")


# ============================================================
# SYSTEM FUNCTIONS
# ============================================================

def has_battery():
    return psutil.sensors_battery() is not None


def find_steam():
    registry_keys = [
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Valve\Steam"),
    ]

    for hive, key_path in registry_keys:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                for value_name in ("SteamPath", "InstallPath"):
                    try:
                        path, _ = winreg.QueryValueEx(key, value_name)

                        steam_exe = os.path.join(path, "steam.exe")

                        if os.path.isfile(steam_exe):
                            return steam_exe

                    except FileNotFoundError:
                        continue

        except FileNotFoundError:
            continue

    return None


# ============================================================
# APPLICATION
# ============================================================

chosen = False

try:
    import webview

    print("APP_DIR:", APP_DIR)
    print("HTML exists:", os.path.exists(INDEX))
    print("CONFIG:", settings)

    class Api:

        def choose(self, choice, desktop_console=False):
            global chosen
        
            if choice == "explorer":
                chosen = True
                os.startfile("explorer.exe")
                window.destroy()
                return
        
            elif choice == "steam":
        
                # Desktop mode + Steam console
                if STEAM_DESKTOP_CONSOLE and desktop_console:
                    steam_exe = find_steam()
        
                    if not steam_exe:
                        chosen = True
                        os.startfile("explorer.exe")
        
                        ctypes.windll.user32.MessageBoxW(
                            None,
                            "Steam is not detected on your device.",
                            "Error",
                            0x10
                        )
        
                        window.destroy()
                        return
        
                    print("[STEAM] Launching desktop mode with console")
                    subprocess.Popen([steam_exe, "-console"])
        
                # Normal Big Picture mode
                elif USE_STEAM_URLS:
                    print("[STEAM] Using Steam URL")
                    os.startfile("steam://open/bigpicture")
        
                else:
                    print("[STEAM] Checking registry")
        
                    steam_exe = find_steam()
        
                    if not steam_exe:
                        chosen = True
                        os.startfile("explorer.exe")
        
                        ctypes.windll.user32.MessageBoxW(
                            None,
                            "Steam is not detected on your device.",
                            "Error",
                            0x10
                        )
        
                        window.destroy()
                        return
        
                    print("[STEAM] Found:", steam_exe)
                    subprocess.Popen([steam_exe, "-bigpicture"])
        
                chosen = True
                window.destroy()
                return

        def has_battery(self):
            return has_battery()
        def steam_desktop_console_available(self):
            return STEAM_DESKTOP_CONSOLE
        def launch_action(self, action):

            if action == "cmd":
                subprocess.Popen(
                    ["cmd.exe"],
                    cwd=os.path.join(
                        os.environ["WINDIR"],
                        "System32"
                    ),
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )

            elif action == "settings":
                os.startfile("ms-settings:")

        def power_action(self, action):
            global chosen

            if action not in ("logoff", "restart", "shutdown"):
                print("[POWER] Unknown action:", action)
                return

            if not INITIALIZE_SHUTDOWNS:
                print("[POWER] Shutdown commands are disabled in debug.cfg")

                ctypes.windll.user32.MessageBoxW(
                    None,
                    "Power commands are disabled in debug.cfg.",
                    "Debug Mode",
                    0x40
                )
                chosen = True
                window.destroy()
                return

            commands = {
                "logoff": ["shutdown", "/l"],
                "restart": ["shutdown", "/r", "/t", "0"],
                "shutdown": ["shutdown", "/s", "/t", "0"]
            }

            print("[POWER] Executing:", action)

            subprocess.Popen(commands[action])

            chosen = True
            window.destroy()


    window = webview.create_window(
        "BootSelect",
        url=INDEX,
        js_api=Api(),
        fullscreen=True,
    )

    print("Starting window...")

    WEBVIEW_DATA = os.path.join(APP_DIR, "WebView2")
    
    os.makedirs(WEBVIEW_DATA, exist_ok=True)
    
    print("WebView2 data:", WEBVIEW_DATA)
    
    webview.start(
        gui="edgechromium",
        private_mode=False,
        storage_path=WEBVIEW_DATA
    )

    print("Window closed. chosen =", chosen)

    if not chosen:
        os.startfile("explorer.exe")


except Exception:
    traceback.print_exc()

finally:
    wait_for_exit()
