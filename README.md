# Clipboard-Command-Executor (Smart Shell Integration)
A smart Python utility that monitors your clipboard for shell commands (like git, npm, python, etc.) and prompts you to execute them in your preferred Command Prompt window. Includes features like terminal selection, typo correction, command safety checks, duplicate prevention, and execution logging.

✨ **Features**
✅ Clipboard Monitoring – Watches clipboard for likely shell commands

⚡ Smart Suggestions – Auto-corrects small typos in known commands

🛑 Dangerous Command Detection – Blocks risky commands like rm, del, shutdown, etc.

💻 Multiple Terminal Handling – Choose from existing CMD windows or open a new one

🔁 Duplicate Guard – Prevents repeated execution of the same command

🧠 UI Prompts – User-friendly prompts using pymsgbox

📜 Execution Logging – Logs all commands with status and timestamp

🧲 System Tray Support – Easily pause/resume via tray icon (optional)

📦 **Requirements**
Install dependencies using pip:
pip install pyperclip pygetwindow pymsgbox pyautogui psutil
pip install pystray pillow

🚀 **How It Works**
1.Copy a shell command to clipboard

2.You'll be prompted: "Do you want to run this command?"

3.If accepted, it checks for existing CMD windows

4.You can:

   Select an existing window

   Leave blank to open a new terminal

   Cancel to abort

5.The command is validated, optionally corrected, and executed

6.Every command is logged in a file (command_log.txt)
