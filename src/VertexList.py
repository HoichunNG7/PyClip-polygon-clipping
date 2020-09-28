class VertexList:
    def __init__(self, main_polygon=None, clipping_polygon=None):
        self.main_list = []
        self.clipping_list = []
        self._generate_lists(main_polygon, clipping_polygon)

    def _generate_lists(self, m_polygon, c_polygon):
        pass

    def find_crossing_of_segments(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        # TODO: Collinear segment case
        if ax1 > ax2:
            ax1, ax2 = ax2, ax1
            ay1, ay2 = ay2, ay1
        if bx1 > bx2:
            bx1, bx2 = bx2, bx1
            by1, by2 = by2, by1

        if bx1 > ax2 or bx2 < ax1:
            return None

        # l1: ak1 * x + ak2 * y + ak3 = 0  |  l2: bk1 * x + bk2 * y + bk3 = 0
        ak1 = ay2 - ay1
        ak2 = ax1 - ax2
        ak3 = ax2 * ay1 - ax1 * ay2
        bk1 = by2 - by1
        bk2 = bx1 - bx2
        bk3 = bx2 * by1 - bx1 * by2

        temp = ak1 * bk2 - bk1 * ak2
        target_x = (bk3 * ak2 - ak3 * bk2) / temp
        target_y = (ak3 * bk1 - bk3 * ak1) / temp

        if ax1 <= target_x <= ax2 and bx1 <= target_x <= bx2:
            return target_x, target_y
        else:
            return None


class Vertex:
    def __init__(self, x, y, next_=None, pre=None, link=None):
        self.x = x
        self.y = y
        self.next = next_
        self.pre = pre
        self.mutual_link = link
