"""

BetterLogs - CheatBetter

Custom Logging Utility

"""

import logging
import typing
from datetime import datetime

import colorama.initialise
from colorama import Fore, Style


class Logger:
    """

    Logger : Base logger class
        :arg name
        :type str
        :arg base_color
        :type colorama.Fore
        :arg base_style
        :type colorama.Style
        :arg time
        :type bool

    """

    def __init__(self, name: str, base_color: Fore, base_style: Style, time: bool, time_color: Fore, time_style: Style):
        self.name = name
        self.color = base_color
        self.style = base_style
        self.time = time
        self.time_color = time_color
        self.time_style = time_style

    """
    
    log : Basic logging function
        :arg msg
        :type str
    
    """

    def log(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + Fore.GREEN + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + Fore.GREEN + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def log_color(self, msg: str, color: Fore) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def log_color_style(self, msg: str, color: Fore, style: Style) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + color + style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + style + msg + Fore.RESET + Style.RESET_ALL)

    def log_custom(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def debug(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + Fore.LIGHTBLACK_EX + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + Fore.LIGHTBLACK_EX + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def debug_color(self, msg: str, color: Fore) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def debug_color_style(self, msg: str, color: Fore, style: Style) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(self.time_style + self.time_color + "[" + date_time_str + "]" + f"({self.name}): " + color + style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + style + msg + Fore.RESET + Style.RESET_ALL)

    def debug_custom(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def warning(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + Fore.YELLOW + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + Fore.YELLOW + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def warning_color(self, msg: str, color: Fore) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def warning_color_style(self, msg: str, color: Fore, style: Style) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + style + msg + Fore.RESET + Style.RESET_ALL)

    def warning_custom(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def error(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + Fore.RED + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + Fore.RED + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def error_color(self, msg: str, color: Fore) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def error_color_style(self, msg: str, color: Fore, style: Style) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + style + msg + Fore.RESET + Style.RESET_ALL)

    def error_custom(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def critical(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)

    def critical_color(self, msg: str, color: Fore) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + self.style + msg + Fore.RESET + Style.RESET_ALL)

    def critical_color_style(self, msg: str, color: Fore, style: Style) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + color + style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + color + style + msg + Fore.RESET + Style.RESET_ALL)

    def critical_custom(self, msg: str) -> typing.Any:
        if self.time:
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            print(
                self.time_style + self.time_color +"[" + date_time_str + "]" + f"({self.name}): " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)
        else:
            print(f"[{self.name}]: " + self.color + self.style + msg + Fore.RESET + Style.RESET_ALL)