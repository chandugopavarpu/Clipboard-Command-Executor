import pyperclip
import time
import subprocess
import pygetwindow as gw
import pymsgbox
import pyautogui
import psutil
import threading
import sys
import os
import datetime
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

monitoring = True
last_clipboard = ""

def is_likely_command(text):
    return text.startswith(('git', 'npm', 'python', 'cd', './', 'mvn', 'java', 'ls', 'dir', 'pip'))

def get_cmd_windows():
    cmd_pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] and 'cmd' in p.info['name'].lower()]
    all_windows = gw.getAllWindows()
    return [w for w in all_windows if w.visible and (
        'Command Prompt' in w.title or
        any(str(pid) in w.title for pid in cmd_pids) or
        w.title.startswith('C:\\')
    )]

def ask_user_to_run(command):
    response = pymsgbox.confirm(
        text=f"Do you want to run this command in Command Prompt?\n\n{command}",
        title="Run Command?",
        buttons=["Yes", "No"]
    )
    return response == "Yes"

def ask_user_which_window(windows):
    names = [f"{i+1}: {win.title}" for i, win in enumerate(windows)]
    choice = pymsgbox.prompt(
        text="Multiple Command Prompt windows detected.\n\nSelect number to target, or leave blank to open a new one:\n\n" + "\n".join(names),
        title="Choose CMD Window"
    )
    if choice is None or choice.strip() == "":
        return "new"
    elif choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(windows):
            return index
    return "invalid"

def run_command_in_new_terminal(command):
    subprocess.Popen(f'start cmd.exe /k "{command}"', shell=True)

def run_in_existing_window(window, command):
    try:
        window.activate()
        time.sleep(1)
        pyautogui.typewrite(command)
        pyautogui.press('enter')
    except Exception as e:
        pymsgbox.alert(f"❌ Failed to send to existing window:\n{e}\nRunning in new window instead.")
        run_command_in_new_terminal(command)

def log_execution(command, status, target):
    with open("execution_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {status}: '{command}' → {target}\n")

def monitor_clipboard():
    global last_clipboard, monitoring
    print("📋 Clipboard monitor running (CMD version)... Press Ctrl+C to exit.")
    while True:
        if monitoring:
            text = pyperclip.paste().strip()
            if text != last_clipboard and is_likely_command(text):
                last_clipboard = text
                if ask_user_to_run(text):
                    cmd_windows = get_cmd_windows()
                    if cmd_windows:
                        selected = ask_user_which_window(cmd_windows)
                        if selected == "new":
                            run_command_in_new_terminal(text)
                            log_execution(text, "Executed", "New CMD")
                        elif isinstance(selected, int):
                            run_in_existing_window(cmd_windows[selected], text)
                            log_execution(text, "Executed", cmd_windows[selected].title)
                        else:
                            pymsgbox.alert("❌ Invalid selection. Command not run.")
                    else:
                        run_command_in_new_terminal(text)
                        log_execution(text, "Executed", "New CMD")
        time.sleep(1)

# 🧠 System Tray Setup
def create_image():
    # Create a visible black square icon on white background
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="black")
    draw.text((20, 20), "CMD", fill="white")
    return image


def toggle_monitoring(icon, item):
    global monitoring
    monitoring = not monitoring
    icon.update_menu()

def quit_app(icon, item):
    icon.stop()
    print("👋 Exiting...")
    os._exit(0)

def main():
    tray_icon = Icon("ClipboardMonitor")
    tray_icon.icon = create_image()
    tray_icon.menu = Menu(
        MenuItem(lambda item: "Pause Monitoring" if monitoring else "Resume Monitoring", toggle_monitoring),
        MenuItem("Quit", quit_app)
    )

    threading.Thread(target=monitor_clipboard, daemon=True).start()
    tray_icon.run_detached()

if __name__ == "__main__":
    main()
