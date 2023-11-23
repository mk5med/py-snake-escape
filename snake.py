class Snake:
    def __init__(self, pos):
        self.pos = pos  # list with 2 items [x, y]

    def generate_next_pos(self, grid):
        """Updates the pos of the snake so that it moves closer to the iguana. Returns true if eats iguana, false else"""
        iguana_pos = grid.iguana_pos
        pos_diff = [iguana_pos[0] - self.pos[0], iguana_pos[1] - self.pos[1]]
        if abs(pos_diff[0]) >= abs(
            pos_diff[1]
        ):  # if closer via x will always move 1 closer there
            self.pos = [
                self.pos[0] + pos_diff[0] // abs(pos_diff[0]),
                self.pos[1],
            ]  # moves 1 closer in x (column)
        else:
            self.pos = [
                self.pos[0],
                self.pos[1] + pos_diff[1] // abs(pos_diff[1]),
            ]  # moves 1 closer in y (row)
        if self.pos == iguana_pos:
            return True
        else:
            return False
