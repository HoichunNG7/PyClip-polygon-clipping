from Polygon import Polygon


def find_crossing_of_segments(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
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


def judge_crossing_type(m_back, m_front, c_back, c_front) -> int:
    main_vector = (m_front.x - m_back.x, m_front.y - m_back.y)
    clipping_vector = (c_back.y - c_front.y, c_front.x - c_back.x)

    if main_vector[0] * clipping_vector[0] + main_vector[1] * clipping_vector[1] > 0:  # out-crossing
        return 1
    else:  # in-crossing
        return 0


class VertexList:
    def __init__(self, main_polygon=None, clipping_polygon=None):
        self.main_list = []
        self.clipping_list = []
        self.crossing_list = []
        self.crossing_count = 0
        self._generate_lists(main_polygon, clipping_polygon)

    def _generate_lists(self, m_polygon: Polygon, c_polygon: Polygon):
        # TODO: Crossing at a vertex case

        insertion_list = []  # Crossings to be inserted

        # Append all vertexes in main polygon
        for m_ring in m_polygon.all_rings:
            m_length = len(m_ring)
            if m_length == 0:
                continue

            m_head_vertex = Vertex(m_ring[0][0], m_ring[0][1])
            self.main_list.append(m_head_vertex)
            m_old_vertex = m_head_vertex

            for i in range(1, m_length):
                m_node = m_ring[i]
                m_vertex = Vertex(m_node[0], m_node[1])
                self.main_list.append(m_vertex)
                if m_old_vertex is not None:
                    m_old_vertex.next = m_vertex
                m_old_vertex = m_vertex

            m_old_vertex.next = m_head_vertex  # Close a cycle chain

        # Append all vertexes in clipping polygon
        for c_ring in c_polygon.all_rings:
            c_length = len(c_ring)
            if c_length == 0:
                continue

            c_head_vertex = Vertex(c_ring[0][0], c_ring[0][1])
            self.clipping_list.append(c_head_vertex)
            c_old_vertex = c_head_vertex

            for i in range(1, c_length):
                c_node = c_ring[i]
                c_vertex = Vertex(c_node[0], c_node[1])
                self.clipping_list.append(c_vertex)
                if c_old_vertex is not None:
                    c_old_vertex.next = c_vertex
                c_old_vertex = c_vertex

            c_old_vertex.next = c_head_vertex  # Close a cycle chain

        # Find and insert crossings
        m_length = len(self.main_list)
        c_length = len(self.clipping_list)

        for i in range(0, m_length):
            m_back = self.main_list[i]
            m_front = m_back.next
            for j in range(0, c_length):
                c_back = self.clipping_list[j]
                c_front = c_back.next
                crossing = find_crossing_of_segments(m_back.x, m_back.y, m_front.x, m_front.y, c_back.x, c_back.y, c_front.x, c_front.y)

                if crossing is not None:
                    # print('mb-', m_back.x, 'mf-', m_front.x, 'cb-', c_back.x, 'cf-', c_front.x)
                    # print('mb-', m_back.y, 'mf-', m_front.y, 'cb-', c_back.y, 'cf-', c_front.y)
                    # print('crossing: id-', self.crossing_count, '  position-', crossing, '  i-', i, '  j-', j)
                    m_vertex = Vertex(crossing[0], crossing[1], id_=self.crossing_count)
                    c_vertex = Vertex(crossing[0], crossing[1], id_=self.crossing_count)
                    if judge_crossing_type(m_back, m_front, c_back, c_front) == 1:
                        m_vertex.type, c_vertex.type = 1, 1
                    else:
                        m_vertex.type, c_vertex.type = 0, 0
                    m_vertex.mutual_link = c_vertex
                    c_vertex.mutual_link = m_vertex

                    self.crossing_list.append(m_vertex)
                    self.crossing_count = self.crossing_count + 1

                    insertion_list.append((m_vertex, 0, m_back))
                    insertion_list.append((c_vertex, 1, c_back))

        for cmd in insertion_list:
            self._vertex_list_insertion(cmd[0], cmd[1], cmd[2])

        # print('Main List: ', len(self.main_list))
        # print('Clipping List: ', len(self.clipping_list))

    def _vertex_list_insertion(self, crossing, list_judge: int, head):
        if list_judge == 0:
            current_list = self.main_list
        elif list_judge == 1:
            current_list = self.clipping_list
        else:
            current_list = None

        x = crossing.x
        vertex_in_list = head
        last_vertex_in_list = head
        if x > head.x:
            while x > vertex_in_list.x:
                last_vertex_in_list = vertex_in_list
                vertex_in_list = vertex_in_list.next
        else:
            while x < vertex_in_list.x:
                last_vertex_in_list = vertex_in_list
                vertex_in_list = vertex_in_list.next

        insert_pos = current_list.index(vertex_in_list)
        current_list.insert(insert_pos, crossing)
        last_vertex_in_list.next = crossing
        crossing.next = vertex_in_list


class Vertex:
    def __init__(self, x, y, id_=-1,  next_=None, link=None):
        self.x = x
        self.y = y
        self.id = id_
        self.type = -1  # in-crossing - 0 or out-crossing - 1
        self.next = next_
        self.mutual_link = link
