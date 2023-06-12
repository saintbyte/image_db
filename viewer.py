#!/usr/bin/env python3

from dotenv import load_dotenv

from repositories.image.sqllite_db import Sqllite3ImageRepository

from tkinter import Tk, Frame, Menu
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

load_dotenv()

class Application(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.master.title("Простое меню")
        menubar = Menu(self.master, tearoff=0)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Открыть...", command=self.openImageDBFile)
        fileMenu.add_command(label="Выход", command=self.onExit)
        menubar.add_cascade(label="Файл", menu=fileMenu)

    def openImageDBFile(self):
        filetypes = (
            ('sqlite databases', '*.sqlite*'),
            ('All files', '*.*')
        )
        filename = fd.askopenfilename(
            title='Open files',
            initialdir='.',
            filetypes=filetypes,
            multiple=False,
        )
        showinfo(
            title='Selected Files',
            message=filename
        )
        if not filename:
            return
        image_db = Sqllite3ImageRepository(filename, False)
        if not image_db.is_image_fb():
            showinfo(
                title='Selected Files',
                message="Its not image db"
            )


    def onExit(self):
        self.quit()


def main():
    root = Tk()
    root.title("Image_DB_viewer")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    _ = Application()
    root.mainloop()


if __name__ == "__main__":
    main()
