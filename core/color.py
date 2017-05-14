# _*_ coding: utf-8 _*_

"""
@file: color.py
@time: 2017/5/6 下午4:26
@author: pigbreeder
"""

import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_PINK = 0x05  # text color contains red.
FOREGROUND_YELLOW = 0x06  # text color contains red.
FOREGROUND_INTENSITY = 0x08  # text color is intensified.
BACKGROUND_BLUE = 0x10  # background color contains blue.
BACKGROUND_GREEN = 0x20  # background color contains green.
BACKGROUND_RED = 0x40  # background color contains red.
BACKGROUND_INTENSITY = 0x80  # background color is intensified.


class BaseColor():
    @staticmethod
    def print_red_text(print_text): pass

    @staticmethod
    def print_green_text(print_text): pass

    @staticmethod
    def print_blue_text(print_text): pass

    @staticmethod
    def print_yellow_text(print_text): pass

    @staticmethod
    def print_pink_text(print_text): pass


class LinuxColor(BaseColor):
    @staticmethod
    def print_red_text(print_text):
        print("\033[1;31;40m" + print_text + "\033[0m")

    @staticmethod
    def print_green_text(print_text):
        print("\033[1;32;40m" + print_text + "\033[0m")

    @staticmethod
    def print_blue_text(print_text):
        print("\033[1;34;40m" + print_text + "\033[0m")

    @staticmethod
    def print_yellow_text(print_text):
        print("\033[1;33;40m" + print_text + "\033[0m")

    @staticmethod
    def print_pink_text(print_text):
        print("\033[1;35;40m" + print_text + "\033[0m")


class WindowsColor(BaseColor):
    @staticmethod
    def set_cmd_color(color):
        ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
            for information on Windows APIs.'''
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    @staticmethod
    def reset_color():
        WindowsColor.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    @staticmethod
    def print_red_text(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()

    @staticmethod
    def print_green_text(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()

    @staticmethod
    def print_blue_text(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()

    @staticmethod
    def print_yellow_text(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()

    @staticmethod
    def print_pink_text(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_PINK | FOREGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()
    @staticmethod
    def print_red_text_with_blue_bg(print_text):
        WindowsColor.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print(print_text)
        WindowsColor.reset_color()
