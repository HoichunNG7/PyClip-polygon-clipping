from tkinter import *
from Polygon import Polygon


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.last_x, self.last_y = -1, -1
        self.first_x, self.first_y = -1, -1
        self.color = 'red'
        self.master = master
        self.pack()

        self.main_polygon = Polygon()
        self.clipping_polygon = Polygon()
        self.current_polygon = -1

        self.create_widget()

    def create_widget(self):
        self.canvas = Canvas(self, width=720, height=540, bg='#FFFFFF')
        self.canvas.bind('<Button-3>', self.draw_last_edge)
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
            self.current_polygon = 0
            self.color = 'red'
            self.reset_last_coord()
            self.canvas.bind('<Button-1>', self.draw_new_vertex)
        elif name == 'window':
            self.current_polygon = 1
            self.color = 'blue'
            self.reset_last_coord()
            self.canvas.bind('<Button-1>', self.draw_new_vertex)
        elif name == 'reset':
            self.canvas.delete('all')
            self.reset_last_coord()
            self.reset_first_coord()
            self.main_polygon = Polygon()
            self.clipping_polygon = Polygon()

    def reset_last_coord(self):
        self.last_x = -1
        self.last_y = -1

    def reset_first_coord(self):
        self.first_x = -1
        self.first_y = -1

    def draw_new_vertex(self, event):
        if self.first_x == -1:  # Store the ring's 1st vertex
            self.first_x, self.first_y = event.x, event.y

        if self.current_polygon == 0:
            self.main_polygon.add_vertex(event.x, event.y)
        elif self.current_polygon == 1:
            self.clipping_polygon.add_vertex(event.x, event.y)

        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill=self.color)
        if self.last_x != -1:
            self.canvas.create_line(self.last_x,  self.last_y, event.x, event.y, fill=self.color)

        self.last_x, self.last_y = event.x, event.y

    def draw_last_edge(self, event):
        if self.first_x == -1:
            return

        if self.current_polygon == 0:
            self.main_polygon.close_ring()
        elif self.current_polygon == 1:
            self.clipping_polygon.close_ring()

        self.canvas.create_line(self.last_x, self.last_y, self.first_x, self.first_y, fill=self.color)
        self.reset_last_coord()
        self.reset_first_coord()


def main():
    root = Tk()
    root.title('PyClip - by Hoichun NG')
    root.iconphoto(False, PhotoImage(file='img/icon.png'))
    app = Application(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
