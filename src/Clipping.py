from VertexList import VertexList as Vlist
from Polygon import Polygon


class WeilerAthertonClipping:
    def __init__(self, v_list=None):
        self.v_list = v_list
        self.new_polygon = Polygon()

    def exec_clipping(self):
        if self.v_list is None:
            return

        in_list = self.v_list.crossing_in_list
        out_list = self.v_list.crossing_out_list
        while len(in_list) != 0:
            start = in_list[0]
            current = start.next
            flag = 0
            self.new_polygon.add_vertex(start.x, start.y)

            while current != start:
                self.new_polygon.add_vertex(current.x, current.y)
                if flag == 0:  # Next crossing will be in out_list
                    pass
                else:  # Next crossing will be in in_list
                    pass

            self.new_polygon.close_ring()

        return
