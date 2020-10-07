from VertexList import VertexList as Vlist, Vertex
from Polygon import Polygon


class WeilerAthertonClipping:
    def __init__(self, v_list: Vlist):
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

    def _search_in_vertex(self) -> Vertex:
        main_top_x = -1
        main_top = None
        clipping_top = None

        for v in self.v_list.main_list:
            if v.x > main_top_x:
                main_top = v
                main_top_x = v.x

        clip_top_x = -1
        for v in self.v_list.clipping_list:
            if v.x > clip_top_x:
                clipping_top = v
                clip_top_x = v.x

        if clipping_top < main_top:  # The rightmost vertex is from main polygon
            pass
        else:  # The rightmost vertex is from clipping polygon
            pass
