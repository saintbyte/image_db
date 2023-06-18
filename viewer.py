#!/usr/bin/env python3

from dotenv import load_dotenv

from repositories.image.sqllite_db import Sqllite3ImageRepository

from tkinter import Tk, Frame, Menu, Button, Label
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image

load_dotenv()


class Application(Frame):
    image = None
    image_area = None
    control_area = None

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

        self.image_area = Frame(self.master, background="red")
        self.image_area.place(relx=0.0, rely=0.0, relheight=0.8, relwidth=1)
        img = ImageTk.PhotoImage(Image.open("/home/sb/projects/ya_disk_list/dataset/1/2800_2900/DSCF9364 (2).JPG"))
        self.image = Label(self.image_area, text="12312")
        #self.image.place(relx=0, rely=0, relheight=1, relwidth=1)
        #self.image.pack()
        self.control_area = Frame(self.master,  background="green", height=140)
        self.control_area.place(relx=0.0, rely=0.8, relheight=1, relwidth=1)
        Button(self.control_area, text='Back', command=self.Back, bg='light blue').place(x=230, y=40)
        Button(self.control_area, text='Next', command=self.Next, bg='light blue').place(x=1000, y=40)

    def openImageDBFile(self):
        filetypes = (
            ('sqlite databases', '*.sqlite?'),
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
            return

    def onExit(self):
        self.quit()

    def Back(self):
        pass

    def Next(self):
        pass



def main():
    root = Tk()
    root.title("Image_DB_viewer")
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    _ = Application()
    root.mainloop()


if __name__ == "__main__":
    main()
