from tkinter import *
from Polygon import Polygon
from VertexList import VertexList as Vlist
from Clipping import WeilerAthertonClipping as WAclip


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.last_x, self.last_y = -1, -1
        self.first_x, self.first_y = -1, -1
        self.color = 'red'
        self.operation_flag = 0
        self.master = master
        self.pack()

        self.main_polygon = Polygon()
        self.clipping_polygon = Polygon()
        self.current_polygon = -1

        self.vertex_list = None
        self.clipping = None

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
        self.btn_clipping.bind('<Button-1>', self.event_manager)

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
            self.reset_everything()
        elif name == 'clipping':
            if self.operation_flag == 0:
                self.vertex_list = Vlist(self.main_polygon, self.clipping_polygon)
                self.draw_crossings(self.vertex_list.crossing_list)
                self.clipping = WAclip(self.vertex_list)
                self.operation_flag = self.operation_flag + 1
            elif self.operation_flag == 1:
                self.clipping.exec_clipping()  # Operate polygon clipping
                self.draw_polygon(self.clipping.new_polygon, line_width=2)
                self.operation_flag = self.operation_flag + 1
            elif self.operation_flag == 2:
                new_polygon = self.clipping.new_polygon
                self.reset_everything()
                self.main_polygon = new_polygon
                self.draw_polygon(self.main_polygon, color='red')

    def reset_last_coord(self):
        self.last_x = -1
        self.last_y = -1

    def reset_first_coord(self):
        self.first_x = -1
        self.first_y = -1

    def reset_everything(self):
        self.canvas.delete('all')
        self.operation_flag = 0
        self.reset_last_coord()
        self.reset_first_coord()
        self.main_polygon = Polygon()
        self.clipping_polygon = Polygon()
        self.vertex_list = None
        self.clipping = None

    def draw_new_vertex(self, event):
        if self.operation_flag != 0:
            return

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

    def draw_crossings(self, crossing_list: list):
        for node in crossing_list:
            if node.type == 1:
                self.canvas.create_oval(node.x - 5, node.y - 5, node.x + 5, node.y + 5, fill='black')
            else:
                self.canvas.create_oval(node.x - 5, node.y - 5, node.x + 5, node.y + 5, fill='green')

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

    def draw_polygon(self, polygon: Polygon, line_width=1, color='black'):
        for ring in polygon.all_rings:
            if len(ring) == 0:
                continue
            old_node = None

            for node in ring:
                self.canvas.create_oval(node[0] - 5, node[1] - 5, node[0] + 5, node[1] + 5, fill=color)

                if old_node is not None:
                    self.canvas.create_line(old_node[0], old_node[1], node[0], node[1], fill=color, width=line_width)
                old_node = node

            self.canvas.create_line(old_node[0], old_node[1], ring[0][0], ring[0][1],fill=color, width=line_width)


def main():
    root = Tk()
    root.title('PyClip - by Hoichun NG')
    root.iconphoto(False, PhotoImage(file='img/icon.png'))
    app = Application(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
