from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.x = 0
        self.y = 0
        self.fgcolor = 'red'
        self.master = master
        self.pack()
        self.canvas = Canvas(self, width=600, height=400, bg='#FFFFFF')
        self.create_widget()

    def create_widget(self):
        self.canvas.pack()


def main():
    root = Tk()
    root.title('PyClip - by Hoichun NG')
    app = Application(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
