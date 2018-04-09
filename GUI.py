import tkinter as tk

class GUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.__create_window()
        self.component_arr = []

    def run(self):
        self.add_button(text="關閉程式", command_func=self.window.destroy)
        for compoent in self.component_arr:
            compoent.pack()
        self.__create()

    def __create_window(self, size="400x600", resizable=False):
        self.window.title("BI 作業")
        self.window.geometry(size)
        if not resizable:
            self.window.resizable(0, 0)
    def add_button(self,text, command_func):
        btn = tk.Button(self.window, text=text, command=command_func, height=2, width=50)
        btn.config(font = ("Courier", 20))
        self.component_arr.append(btn)
    def add_label(self, text):
        label = tk.Label(self.window, text=text, height=2)
        label.config(font=("Courier", 25))
        self.component_arr.append(label)

    def __create(self):
        self.window.mainloop()

    @staticmethod
    def popupmsg(msg):
        LARGE_FONT = ("Verdana", 12)
        NORM_FONT = ("Helvetica", 10)
        SMALL_FONT = ("Helvetica", 8)
        popup = tk.Tk()
        popup.geometry("100x100")
        popup.wm_title("提醒")
        label = tk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="OK", command=popup.destroy)
        B1.pack()
        popup.mainloop()