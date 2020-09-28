class Polygon:
    def __init__(self):
        self.top_vertex_index = -1
        self.top_x = 100000
        self.top_y = 100000
        self.current_ring_index = 0
        self.ring_directions = []
        self.all_rings = []
        self.all_rings.append([])

    def add_vertex(self, x, y):
        if x < 0 or y < 0:
            return

        # print('x: ', x, 'y: ', y)
        if x < self.top_x:
            self.top_x = x
            self.top_y = y
            self.top_vertex_index = len(self.all_rings[self.current_ring_index])

        self.all_rings[self.current_ring_index].append((x, y))

    def close_ring(self):
        direction = self.judge_ring_direction()
        self.ring_directions.append(direction)
        print('direction: ', direction)
        # print('ring_id: ', self.current_ring_index)

        self.current_ring_index = self.current_ring_index + 1
        self.all_rings.append([])
        self.top_vertex_index = -1
        self.top_x = 100000

    def judge_ring_direction(self):  # Output: 1-clockwise, 0-counter-clockwise
        ring = self.all_rings[self.current_ring_index]
        vertex_num = len(ring)
        next_x, next_y = ring[(self.top_vertex_index + 1) % vertex_num]
        previous_x, previous_y = ring[(self.top_vertex_index - 1 + vertex_num) % vertex_num]

        if next_x == self.top_x:  # If next edge is parallel to y-axis
            if next_y > self.top_y:
                return 1
            else:
                return 0
        if previous_x == self.top_x:  # If last edge is parallel to y-axis
            if previous_y > self.top_y:
                return 0
            else:
                return 1

        next_slope = (next_y - self.top_y) / (next_x - self.top_x)
        previous_slope = (previous_y - self.top_y) / (previous_x - self.top_x)
        if next_slope > previous_slope:
            return 0
        else:
            return 1
