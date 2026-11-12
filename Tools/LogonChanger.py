
import os
import sys
import winreg
import tkinter as tk
from tkinter import messagebox, filedialog

# ============================================================
# PATHS
# ============================================================

APP_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

REG_PATH = r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon"

selected_exe = ""


# ============================================================
# REGISTRY
# ============================================================

def set_shell(value):
    try:
        with winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER,
            REG_PATH,
            0,
            winreg.KEY_SET_VALUE
        ) as key:

            winreg.SetValueEx(
                key,
                "Shell",
                0,
                winreg.REG_SZ,
                value
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


# ============================================================
# ACTIONS
# ============================================================

def browse_exe():
    global selected_exe

    path = filedialog.askopenfilename(
        title="Select Logon Application",
        filetypes=[
            ("Executable files", "*.exe"),
            ("All files", "*.*")
        ]
    )

    if not path:
        return

    selected_exe = os.path.abspath(path)

    exe_label.config(
        text=selected_exe,
        fg="#75a9e8"
    )

    update_status()


def set_as_logon():
    if not selected_exe:
        messagebox.showwarning(
            "No Application Selected",
            "Please select an executable first."
        )
        return

    if not os.path.isfile(selected_exe):
        messagebox.showerror(
            "File Not Found",
            "The selected executable no longer exists."
        )
        return

    confirmed = messagebox.askyesno(
        "Set Application as Logon",
        f"Are you sure you want to replace Explorer with:\n\n"
        f"{selected_exe}\n\n"
        "WARNING:\n"
        "Windows will launch this application instead of "
        "explorer.exe when you log in.\n\n"
        "If it fails to start or you cannot launch Explorer "
        "again, you may get stuck without your normal desktop "
        "and taskbar.\n\n"
        "Make sure you know how to recover Explorer before continuing."
    )

    if not confirmed:
        return

    shell_path = f'"{selected_exe}"'

    if set_shell(shell_path):
        messagebox.showinfo(
            "Success",
            "The selected application has been configured "
            "as your logon shell.\n\n"
            "The change takes effect after your next sign-in."
        )
        update_status()


def restore_explorer():
    confirmed = messagebox.askyesno(
        "Restore Explorer",
        "Are you sure you want to restore Windows Explorer "
        "as your logon shell?\n\n"
        "This will set the shell back to explorer.exe."
    )

    if not confirmed:
        return

    if set_shell("explorer.exe"):
        messagebox.showinfo(
            "Success",
            "Windows Explorer has been restored as your logon shell.\n\n"
            "The change takes effect after your next sign-in."
        )
        update_status()


def open_app_folder():
    os.startfile(APP_DIR)


# ============================================================
# INTERFACE
# ============================================================


def update_status():
    current = get_shell()

    if current.lower() == "explorer.exe":
        status_label.config(
            text="Current shell: Windows Explorer",
            fg="#75c98b"
        )

    elif selected_exe and current.lower() == f'"{selected_exe}"'.lower():
        status_label.config(
            text="Current shell: Selected application",
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



root = tk.Tk()
root.title("Logon changer")
root.geometry("460x380")
root.resizable(False, False)
root.configure(bg="#17191e")

title = tk.Label(
    root,
    text="Logon changer",
    font=("Segoe UI", 15, "bold"),
    fg="#eeeeee",
    bg="#17191e"
)
title.pack(pady=(20, 8))

subtitle = tk.Label(
    root,
    text="Configure which application starts at logon.",
    font=("Segoe UI", 9),
    fg="#999da7",
    bg="#17191e"
)
subtitle.pack(pady=(0, 14))


# APPLICATION SELECTION

browse_button = tk.Button(
    root,
    text="Browse for Application...",
    font=("Segoe UI", 9, "bold"),
    bg="#303b50",
    fg="white",
    activebackground="#40516d",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=browse_exe,
    width=28,
    height=2
)
browse_button.pack(pady=4)

exe_label = tk.Label(
    root,
    text="No application selected",
    font=("Segoe UI", 8),
    fg="#999da7",
    bg="#17191e",
    wraplength=420
)
exe_label.pack(pady=(4, 12))


# SET SHELL

set_button = tk.Button(
    root,
    text="Set Selected Application as Logon",
    font=("Segoe UI", 10, "bold"),
    bg="#303b50",
    fg="white",
    activebackground="#40516d",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=set_as_logon,
    width=36,
    height=2
)
set_button.pack(pady=4)


# RESTORE EXPLORER

restore_button = tk.Button(
    root,
    text="Restore Explorer",
    font=("Segoe UI", 10, "bold"),
    bg="#303030",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=restore_explorer,
    width=36,
    height=2
)
restore_button.pack(pady=4)


# OPEN FOLDER

folder_button = tk.Button(
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
)
folder_button.place(
    relx=1.0,
    rely=1.0,
    x=-12,
    y=-12,
    anchor="se"
)


status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 9),
    bg="#17191e"
)
status_label.pack(pady=(10, 0))

shell_value_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 8),
    fg="#999da7",
    bg="#17191e",
    wraplength=420,
    justify="center"
)
shell_value_label.pack(pady=(4, 0))

update_status()

root.mainloop()
