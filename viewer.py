#!/usr/bin/env python3

from dotenv import load_dotenv

from tkinter import Tk
from ui.viewer import Application

load_dotenv()


def main():
    root = Tk()
    root.title("Image_DB_viewer")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    _ = Application()
    root.mainloop()


if __name__ == "__main__":
    main()
