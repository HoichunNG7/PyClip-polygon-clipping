from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.last_x = -1
        self.last_y = -1
        self.color = 'red'
        self.master = master
        self.pack()

        self.create_widget()

    def create_widget(self):
        self.canvas = Canvas(self, width=720, height=540, bg='#FFFFFF')
        self.canvas.pack()

        self.btn_object = Button(self, name='object', text='主多边形')
        self.btn_object.pack(side='left', padx=10)
        self.btn_window = Button(self, name='window', text='裁剪多边形')
        self.btn_window.pack(side='left', padx=10)
        self.btn_reset = Button(self, name='reset', text='重置')
        self.btn_reset.pack(side='left', padx=10)
        self.btn_clipping = Button(self, name='clipping', text='裁剪')
        self.btn_clipping.pack(side='right', padx=10)

        self.btn_object.bind('<Button-1>', self.event_manager)
        self.btn_window.bind('<Button-1>', self.event_manager)
        self.btn_reset.bind('<Button-1>', self.event_manager)

    def event_manager(self, event):
        name = event.widget.winfo_name()
        if name == 'object':
            self.color = 'red'
            self.reset_last_coord()
            self.canvas.bind('<Button-1>', self.draw_new_vertex)
        elif name == 'window':
            self.color = 'blue'
            self.reset_last_coord()
            self.canvas.bind('<Button-1>', self.draw_new_vertex)
        elif name == 'reset':
            self.canvas.delete('all')
            self.reset_last_coord()

    def reset_last_coord(self):
        self.last_x = -1
        self.last_y = -1

    def draw_new_vertex(self, event):
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill=self.color)
        if self.last_x != -1:
            self.canvas.create_line(self.last_x,  self.last_y, event.x, event.y, fill=self.color)

        self.last_x, self.last_y = event.x, event.y


def main():
    root = Tk()
    root.title('PyClip - by Hoichun NG')
    root.iconphoto(False, PhotoImage(file='img/icon.png'))
    app = Application(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
