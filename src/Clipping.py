from VertexList import VertexList as Vlist
from Polygon import Polygon


class WeilerAthertonClipping:
    def __init__(self, v_list: Vlist):
        self.v_list = v_list
        self.new_polygon = Polygon()

    def exec_clipping(self):
        if self.v_list is None:
            return

        while True:
            if len(self.v_list.crossing_list) > 0:
                current_node = self.v_list.crossing_list[0]
                flag = current_node.type
                if flag == 1:
                    current_node = current_node.mutual_link

                start_node = current_node
                self.new_polygon.add_vertex(current_node.x, current_node.y)
            else:
                break

            while True:
                current_node = current_node.next
                if current_node.id == start_node.id:
                    self.v_list.delete_crossing_by_id(current_node.id)
                    break

                self.new_polygon.add_vertex(current_node.x, current_node.y)

                if current_node.id < 0:  # polygon vertex
                    continue
                self.v_list.delete_crossing_by_id(current_node.id)
                current_node = current_node.mutual_link  # crossing

            self.new_polygon.close_ring()

        return
