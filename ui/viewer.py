from repositories.image.sqllite_db import Sqllite3ImageRepository
from tkinter import Frame, Menu, Button, Label
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image


class Application(Frame):
    image = None
    image_area = None
    control_area = None
    image_db = None
    def __init__(self):
        super().__init__()
        self.initUI()

    def make_menu(self):
        menubar = Menu(self.master, tearoff=0)
        self.master.config(menu=menubar)
        file_menu = Menu(menubar)
        file_menu.add_command(label="Открыть...", command=self.openImageDBFile)
        file_menu.add_command(label="Выход", command=self.onExit)
        menubar.add_cascade(label="Файл", menu=file_menu)


    def make_work_are(self):
        self.image_area = Frame(self.master, background="red")
        self.image_area.place(relx=0.0, rely=0.0, relheight=0.8, relwidth=1)
        self.image = Label(self.image_area, text="Изображение")
        self.image.pack()
        self.image.place(relx=0, rely=0, relheight=1, relwidth=1)

    def initUI(self):
        self.make_menu()
        self.make_work_are()
        self.control_area = Frame(self.master,  background="green", height=140)
        self.control_area.place(relx=0.0, rely=0.8, relheight=1, relwidth=1)
        Button(self.control_area, text='Back', command=self.Back, bg='light blue').place(x=230, y=40)
        Button(self.control_area, text='Next', command=self.Next, bg='light blue').place(x=1000, y=40)

    def show_image(self, image_record):
        img = ImageTk.PhotoImage(
        Image.open("/home/sb/projects/ya_disk_list/dataset/1/3400_3500/420283681272736676_35852537.jpg"))
        self.image.image = img

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
        self.image_db = Sqllite3ImageRepository(filename, False)
        if not self.image_db.is_image_fb():
            self.image_db = None
            showinfo(
                title='Selected Files',
                message="Its not image db"
            )
            return
        first_image = self.image_db.get_first_image()
        print(first_image)
        self.show_image(first_image)


    def onExit(self):
        self.quit()

    def Back(self):
        pass

    def Next(self):
        pass