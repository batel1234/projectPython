import math
import tkinter as tk
import numpy as np
from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk, ImageGrab
from tkinter import ttk
from tkinter.colorchooser import askcolor


class Edit:
    def __init__(self):
        self.ix = 0
        self.chosen_font = cv2.FONT_HERSHEY_SIMPLEX
        self.chosen_thick = 1
        self.chosen_size = 1
        self.iy = 0
        self.drawing = False
        self.img = None
        self.coloring = (255, 255, 255)
        self.i = 0
        self.sizes = 0
        self.thick = 0

    def draw_shape(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            if self.t == 'c':
                radius = int(math.sqrt((x - self.ix) ** 2 + (y - self.iy) ** 2))
                cv2.circle(self.img, (self.ix, self.iy), radius, self.coloring, 5)
                cv2.imshow("Image editing", self.img)
            elif self.t == 's':
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.coloring, 5)
                cv2.imshow("Image editing", self.img)
            elif self.t == 'l':
                cv2.line(self.img, (self.ix, self.iy), (x, y), self.coloring, 2, cv2.LINE_AA)
                cv2.imshow("Image editing", self.img)

    def save_image(self):  # שמירת התמונה
        # לקבל את השם של הקובץ שהמשתמש בחר לשמור
        filename = filedialog.asksaveasfilename(initialdir="/", title="Save file",
                                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")),
                                                defaultextension="")
        if filename:
            # להשתמש בפונקציה imwrite כדי לשמור את התמונה באותם צבעים
            cv2.imwrite(filename, self.img)

    def shape(self, root, temp):  # שליחה לפונקצית ציור
        self.t = temp
        root.destroy()
        cv2.setMouseCallback("Image editing", self.draw_shape)

    def open_window_shape(self):  # פונקציה לפתיחת חלון הבחירה בצורה לציור
        root = tk.Tk()
        root.title("Choose shape:")
        font_style = tkFont.Font(family="Tahoma", size=10, weight="bold")
        button = tk.Button(root, text="chose color", width=20, height=2, font=font_style,
                           command=lambda: self.color())
        bt1 = tk.Button(root, text="Circle", width=20, height=3, bg="light blue", font=font_style,
                        command=lambda: self.shape(root, 'c'))
        bt2 = tk.Button(root, text="Square", width=20, height=3, bg="light blue", font=font_style,
                        command=lambda: self.shape(root, 's'))
        bt3 = tk.Button(root, text="Line", width=20, height=3, bg="light blue", font=font_style,
                        command=lambda: self.shape(root, 'l'))
        button.grid(row=0, column=0, padx=20, pady=20)
        bt1.grid(row=1, column=0, padx=20, pady=20)
        bt2.grid(row=2, column=0, padx=20, pady=20)
        bt3.grid(row=3, column=0, padx=20, pady=20)

        root.mainloop()
        cv2.waitKey(0)

    def choose_image(self, win):  # פונקציה פותחת את התמונה שבחרנו
        win.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.img = Image.open(win.filename)
        photo = ImageTk.PhotoImage(self.img)
        label1 = Label(win, image=photo)
        label1.img = photo
        cv2.namedWindow("Image editing")
        self.img = cv2.imread(win.filename)
        cv2.imshow("Image editing", self.img)
        cv2.setMouseCallback("Image editing", self.change_color)

    def change_color(self,event, x, y, flags, params):
        if event == cv2.EVENT_RBUTTONDOWN:
            noise = np.random.randint(-50, 50, size=self.img.shape)
            self.img += noise
            self.img[self.img > 255] = 255
            self.img[self.img < 0] = 0
            cv2.imshow("Image editing", self.img)


    def cut_image(self):  # לחתוך תמונה
        self.drawing = False
        def cut(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix, self.iy = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                if self.drawing:
                    self.drawing = False
                    x_min, x_max = min(self.ix, x), max(self.ix, x)
                    y_min, y_max = min(self.iy, y), max(self.iy, y)
                    self.img = self.img[y_min:y_max, x_min:x_max]
                    cv2.imshow("Image editing", self.img)
        cv2.setMouseCallback("Image editing", cut)


    def add_text_to_image(self):  # חלונית להוספת טקסט
        root = Tk()
        root.title("choose text:")
        font_style = tkFont.Font(family="Tahoma", size=5, weight="bold")  # עיצוב של כתב
        s = tk.IntVar()
        t = tk.IntVar()
        self.sizes = ttk.Combobox(root, width=5,
                                  textvariable=s)
        self.thick = ttk.Combobox(root, width=5,
                                  textvariable=t)
        self.sizes['values'] = (1, 2, 3, 4, 5, 6)
        self.thick['values'] = (1, 2, 3, 4, 5, 6)
        self.sizes.state(['readonly'])
        self.sizes.current(0)
        self.thick.current(0)
        self.thick.state(['readonly'])  # בלי יכולת לשנות את הנתונים
        si = Label(root, text="chose size:", font=font_style)  # כותברות לכפתרוים
        th = Label(root, text="chose thick:", font=font_style)
        lbl = Label(root, text="enter text:", font=font_style)
        entry = Entry(root)
        th.grid(row=0, column=1)
        si.grid(row=0, column=0)
        self.sizes.grid(column=0, row=1)
        self.thick.grid(column=1, row=1)
        lbl.grid(row=2, column=0)
        entry.grid(row=2, column=1)
        bt1 = Button(root, text="v", width=5, height=1, bg="light blue",
                     font=font_style, command=lambda: self.texts(entry.get()))  # ,command=lambda : texts
        bt2 = Button(root, text="chose color", width=10, height=1, bg="light blue",
                     font=font_style, command=lambda: self.color())
        bt1.grid(row=3, column=1, padx=0, pady=2)
        bt2.grid(row=3, column=2, padx=0, pady=2)
        root.mainloop()

    def texts(self, text):  # הוספת טקסט
        def add_text(event, x, y, flags, param):
            self.chosen_size = int(self.sizes.get())
            self.chosen_thick = int(self.thick.get())
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.putText(self.img, text, (x, y), self.chosen_font, self.chosen_size, self.coloring,
                            self.chosen_thick)  # קבלת הכתב הפונט הגודל הצבע והעובי
                cv2.imshow("Image editing", self.img)
        cv2.setMouseCallback("Image editing", add_text)

    def color(self):
        global root
        colors = {
        "red": (0, 0, 255),"crimson": (60, 20, 220),"indian red": (92, 92, 205),"brown": (42, 42, 165),"maroon": (0, 0, 128),
        "sienna": (45, 82, 160),"peru": (63, 133, 205),"tan": (140, 180, 210),
        "blue": (255, 0, 0),"navy": (128, 0, 0),"indigo": (130, 0, 75),"purple": (128, 0, 128),
        "magenta": (255, 0, 255),"violet": (238, 130, 238),"plum": (221, 160, 221),"pink": (203, 192, 255),
        "cyan": (255, 255, 0),"turquoise": (208, 224, 64),"powder blue": (230, 224, 176),"sky blue": (235, 206, 135),
        "aquamarine": (212, 255, 127), "teal": (128, 128, 0),"green": (0, 128, 0),"olive": (0, 128, 128),"lime": (0, 255, 0),
        "tomato": (71, 99, 255),"salmon": (114, 128, 250),"coral": (128, 128, 255),"orange": (0, 165, 255),
        "gold": (0, 215, 255),"wheat": (179, 222, 245),"khaki": (140, 230, 240),"yellow": (0, 255, 255),"navajo white": (173, 222, 255),
        "white": (255, 255, 255),"lavender": (250, 200, 200),"silver": (192, 192, 192),
        "gray": (128, 128, 128),"black": (0, 0, 0),"rosy brown": (143, 143, 188)
        }
        def button_click(color):
            global root
            self.coloring = colors[color]
            root.destroy()
        root = Tk()
        root.title("Color Picker")
        for i, color in enumerate(colors):
            button = Button(root, bg=color, width=1, height=1, command=lambda color=color: button_click(color))
            button.grid(row=i // 20, column=i % 20, padx=2, pady=2)
        root.mainloop()


    def Processing_image(self):
        root = tk.Tk()
        root.title("Choose processing:")
        font_style = tkFont.Font(family="Tahoma", size=5, weight="bold")
        quality_label = tk.Label(root, text="Choose image quality:", font=font_style)
        quality_label.grid(row=0, column=0)
        q = tk.StringVar()
        quality = ttk.Combobox(root, width=5, textvariable=q, values=["white&balck", "blur", "edge", "contrast", "original","normal"],
                               state="readonly")
        quality.grid(row=0, column=1)
        bt1 = Button(root, text="v", width=5, height=1, bg="light blue",
                     command=lambda: self.apply_changes(str(quality.get()), root))
        bt1.grid(row=6, column=4)
        self.cancels=self.img
        root.mainloop()


    def apply_changes(self,proc_quality, root):
        if proc_quality == "white&balck":
            self.img =cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)# שחור לבן
            cv2.imshow("Image editing", self.img)
        elif proc_quality == "blur":
            self.img = cv2.GaussianBlur(self.img, (7, 7), 0) #מטושטש
            cv2.imshow("Image editing", self.img)
        elif proc_quality == "contrast":
            self.img = cv2.addWeighted(self.img, 1.5, np.zeros(self.img.shape, self.img.dtype), 3, 3)#בהירות
            cv2.imshow("Image editing", self.img)
        elif proc_quality == "original":
            self.img = cv2.cvtColor(self.img, cv2.COLOR_HSV2BGR)#
            cv2.imshow("Image editing", self.img)
        elif proc_quality == "edge":
            self.img = cv2.Canny(self.img,100,200)
            cv2.imshow("Image editing", self.img)
        elif proc_quality == "normal":
            cv2.imshow("Image editing", self.cancels) #התמונה המקורת
