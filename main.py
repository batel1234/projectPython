from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import cv2
from tkinter.messagebox import askyesno
import image


class Img:
    def __init__(self):
        self.win = Tk()  # יצירת חלונית
        self.win.title("Project")  # שם החלונית
        b = image.Edit()
        def confirm():
            answer = askyesno(title='confirmation',
                              message='Are you sure that you want to exit?')
            if answer:
                self.win.destroy()

        font_style = tkFont.Font(family="Tahoma", size=10, weight="bold")  # עיצוב של כתב
        font_style_title = tkFont.Font(family="Tahoma", size=20, weight="bold")
        self.exiting = Button(self.win, text="exit", width=3, height=1, font=font_style, command=confirm)
        self.label = Label(self.win, text="Painter", font=font_style_title, fg="crimson")
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.c = Label(self.win, text="©batel chacham", width=20, height=3, font=font_style)  # ציור
        self.c.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.button1 = Button(self.win, text="choose image", width=20, bg="pink", height=3, font=font_style,
                              command=lambda:b.choose_image(self.win))  # בחירת תמונה
        self.button2 = Button(self.win, text="Processing", width=20, bg="khaki", height=3, font=font_style,
                              command=lambda: b.Processing_image())  # עיבוד
        self.button3 = Button(self.win, text="cut", width=20, bg="pink", height=3, font=font_style,
                              command=lambda: b.cut_image())  # חיתוך
        self.button4 = Button(self.win, text="Adding text", width=20, bg="khaki", height=3,
                              font=font_style, command=lambda: b.add_text_to_image())  # הוספת טקסט
        self.button5 = Button(self.win, text="Add a shape", width=20, bg="pink", height=3,
                              font=font_style, command=lambda: b.open_window_shape())  # הוספת צורה
        self.button6 = Button(self.win, text="save", width=20, bg="khaki", height=3, font=font_style,
                              command=lambda: b.save_image())  # שמירה
        self.positions()
        self.win.geometry("700x600")
        self.win.mainloop()

    def positions(self):  # ממקם את הכפתורים על המסך
        self.exiting.grid(row=1, column=3, pady=10, padx=20)
        self.button1.grid(row=3, column=0, padx=20, pady=20)
        self.button2.grid(row=3, column=1, padx=20, pady=20)
        self.button3.grid(row=3, column=2, padx=20, pady=20)
        self.button4.grid(row=4, column=0, padx=20, pady=20)
        self.button5.grid(row=4, column=1, padx=20, pady=20)
        self.button6.grid(row=4, column=2, padx=20, pady=20)


a = Img()
