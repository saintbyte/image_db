from repositories.image.sqllite_db import Sqllite3ImageRepository
from tkinter import Frame, Menu, Button, Label, Canvas
from tkinter import filedialog as fd
from tkinter import YES, BOTH, CENTER, N
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image


class Application(Frame):
    image = None
    image_area = None
    control_area = None
    image_db = None
    image_container = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.bind("<Configure>", self.resize)

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
        self.image = Canvas(self.image_area, background="light green",)
        self.image.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.image.pack(expand=YES, fill=BOTH)

    def resize(self):
        print("resize")

    def initUI(self):
        self.make_menu()
        self.make_work_are()
        self.control_area = Frame(self.master, background="green", height=140)
        self.control_area.place(relx=0.0, rely=0.8, relheight=1, relwidth=1)
        Button(self.control_area, text='Back', command=self.Back, bg='light blue').place(x=230, y=40)
        Button(self.control_area, text='Next', command=self.Next, bg='light blue').place(x=1000, y=40)

    def show_image(self, image_record):
        if image_record is None:
            return
        print(image_record)
        #photo = Image.open(image_record["path"])
        #photo = photo.resize((100, 100), Image.ANTIALIAS)
        #photo = ImageTk.PhotoImage(photo)
        photo = ImageTk.PhotoImage(file=image_record["path"])
        if self.image_container is None:
            self.image_container = self.image.create_image(0, 0, anchor='nw', image=photo)
            self.image_container.pack(expand=YES, fill=BOTH)
            self.image.imgref = photo
            return
        # self.image.create_image(50, 50, anchor='nw', fill=BOTH, image=photo)
        # self.image.update()
        self.image.itemconfig(self.image_container, image=photo)
        self.image.imgref = photo

        #self.image.itemconfig(self.image_container, image=photo)
        #self.image.update()
        #self.image.pack()
        """
        img = Image.open(image_record["path"])
        print(img)
        self.image.image = ImageTk.PhotoImage(file = image_record["path"])
        
        self.image.pack()
        self.image.update()
        self.image.pack()

    """

    def openImageDBFile(self):
        filetypes = (
            ('sqlite databases', '*.sqlite3'),
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
        self.show_image(first_image)

    def onExit(self):
        self.quit()

    def Back(self):
        if not self.image_db:
            return
        image = self.image_db.get_prev_image()
        self.show_image(image)

    def Next(self):
        if not self.image_db:
            return
        image = self.image_db.get_next_image()
        self.show_image(image)
