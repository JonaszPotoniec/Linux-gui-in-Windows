import tkinter as tk
import os
import re
from win32com.client import Dispatch

unusualDistrosExecutablesNames = {
    "kali-linux": "kali"
}


def create_shortcut_clicked():
    distroName = re.sub("( )", "", get_distro_name())
    create_shortcut(
        distroName,
        (" " if distroName == "wsl" else " run ") + "\"export DISPLAY=:0 && " + appName.get() + "\""
    )


def refresh_clicked():
    distroMenu['menu'].delete(0, 'end')
    for line in os.popen('wslconfig.exe /l').read().split("\n"):
        line = re.sub("(\x00)", "", line)
        if line.find("Windows Subsystem for Linux Distributions:") == -1 and bool(re.search('[aA-zZ]', line)):
            print(line)
            distroList.append(line)
            distroMenu['menu'].add_command(label=line, command=tk._setit(var, line))

            if line.find("Default") != -1:
                var.set(line)


def install():
    install_window = tk.Toplevel(pady=padding, padx=padding)
    install_window.title("Chose installation method...")

    tk.Label(install_window, text="Chose installation method").pack(pady=padding, padx=padding)
    tk.Button(install_window, text="apt-get (recommended for ubuntu-based distributions)", command=lambda: apt_install(appName.get())).pack(pady=padding, padx=padding)
    tk.Button(install_window, text="dpkg (select from file) WIP", command=install, state="disabled").pack(pady=padding, padx=padding)


def apt_install(package_name):
    print(execute_root_command("apt -y update"))
    print(execute_root_command("apt -y install " + package_name))


def execute_root_command(command):
    distroName = get_distro_name()
    line = os.popen(
        distroName + (" " if distroName == "wsl" else " run ") + "\"echo " + password.get() + " | sudo -S " + command + "\""
    ).read()
    line = re.sub("(\x00)", "", line)
    return line


def get_distro_name():
    try:
        return unusualDistrosExecutablesNames[var.get()]
    except KeyError:
        if var.get() == 'default':
            return "wsl"
        elif var.get().find("Default"):
            return re.sub("\(Default\)", "", var.get())
        else:
            return var.get()


def create_shortcut(distro, target):
    desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
    path = os.path.join(desktop, distro + " - " + appName.get() + ".lnk")
    wDir = r"P:\Media\Media Player Classic"
    icon = r"P:\Media\Media Player Classic\mplayerc.exe"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = distro
    shortcut.Arguments = target
    #shortcut.WorkingDirectory = wDir
    #shortcut.IconLocation = icon
    shortcut.save()


root = tk.Tk()
root.title("linux gui shortcut maker")
padding = 5

tk.Label(root, text="Distribution name").grid(row=0, sticky=tk.W, pady=padding, padx=padding)
tk.Label(root, text="App name").grid(row=1, sticky=tk.W, pady=padding, padx=padding)
tk.Label(root, text="Su password").grid(row=2, sticky=tk.W, pady=padding, padx=padding)

var = tk.StringVar(root)
var.set('default')
distroList = ['default']
distroMenu = tk.OptionMenu(root, var, *distroList)
appName = tk.Entry(root)
password = tk.Entry(root, show="*")

distroMenu.grid(row=0, column=1, columnspan=2, pady=padding, padx=padding)
appName.grid(row=1, column=1, columnspan=2, pady=padding, padx=padding)
password.grid(row=2, column=1, columnspan=2, pady=padding, padx=padding)
refreshButton = tk.Button(root, text="Refresh", command=refresh_clicked).grid(row=3, column=0, pady=padding, padx=padding)
installButton = tk.Button(root, text="Install", command=install).grid(row=3, column=1, pady=padding, padx=padding)
shortcutButton = tk.Button(root, text="Add shortcut", command=create_shortcut_clicked).grid(row=3, column=2, pady=padding, padx=padding)

refresh_clicked()
root.mainloop()