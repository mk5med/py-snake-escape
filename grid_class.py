# Contains class for representing the grid environment
# Uses random to get a random grid initialization
import random
import math
import time  # for sleep
from snake import Snake
import typing

## Helpers for run_round ##
Action = typing.Callable[[typing.Tuple[int, int], int], typing.Tuple[int, int]]
up: Action = lambda pos, size: [pos[0], max(0, pos[1] - 1)]
down: Action = lambda pos, size: [pos[0], min(size - 1, pos[1] + 1)]
left: Action = lambda pos, size: [max(0, pos[0] - 1), pos[1]]
right: Action = lambda pos, size: [min(size - 1, pos[0] + 1), pos[1]]


class GridEnvironment:
    def __init__(self, size=9, num_snakes=5, do_print=True):
        random.seed()  # I guess we seed here?
        self.size = size  # 21*21 grid by default
        self.center = self.size // 2  # the centre position
        self.centre_coord = [self.center, self.center]  # in list form
        self.grid = []  # the actual grid
        self.num_snakes = num_snakes  # number of snakes
        self.snakes = []  # list of snakes
        self.snake_positions = []
        self.iguana_pos = self.centre_coord  # by initialization (will change)

        ## Initialise the map ##
        # Populate the grid
        for i in range(self.size):
            self.grid.append(["-"] * self.size)  # '-' means nothing there
        self.grid[self.center][self.center] = "I"

        self.initialize_snakes()

        # self.goal = [None, None] # To make the goal
        self.initialize_goal()  # To make the goal

        ## Initialise non-map settings ##
        self.iguana_ded = False
        self.iguana_escaped = False

        ## Helpers ##
        self.do_print = do_print

    def initialize_snakes(self):
        """
        Places snakes at random locations on the grid at initialization
        """
        # Try to find a valid location for each snake
        for i in range(self.num_snakes):
            valid_location_found = False
            # Loop until a valid location is found for the snake
            while not valid_location_found:
                # Select a random coordinate on the map
                one_coord = random.randint(0, self.size - 1)

                # Create a list of possible positions
                options = [
                    [0, one_coord],
                    [self.size - 1, one_coord],
                    [one_coord, 0],
                    [one_coord, self.size - 1],
                ]

                # Select one of the options
                location = random.choice(options)  # Either on left, right, top, or bot

                # print(location)
                if (
                    # The current cell position does not contain a snake
                    self.grid[location[1]][location[0]]
                    != "S"
                ):
                    # row, column to x, y (swap)
                    # Set the current cell position
                    self.grid[location[1]][location[0]] = "S"

                    # Create a new snake at the current position
                    temp_snake = Snake(location)
                    self.snakes.append(temp_snake)
                    self.snake_positions.append(temp_snake.pos)

                    # Mark that a position has been found for the current snake
                    valid_location_found = True

    def initialize_goal(self):
        """
        Add the goal onto the grid
        """
        goal_generated = False
        while not goal_generated:
            one_coord = random.randint(0, self.size - 1)
            options = [
                [0, one_coord],
                [self.size - 1, one_coord],
                [one_coord, 0],
                [one_coord, self.size - 1],
            ]
            location = random.choice(options)

            # Check that the goal does not override a snake position
            if self.grid[location[1]][location[0]] != "S":
                self.goal = location
                self.grid[location[1]][location[0]] = "G"
                goal_generated = True

    def check_loss(self):
        """
        Checks if any snake is at the same position as the iguana.

        @returns `True` if loss, `False` else
        """
        for snake in self.snakes:
            if snake.pos == self.iguana_pos:
                self.iguana_ded = True
                self.grid[self.iguana_pos[1]][
                    self.iguana_pos[0]
                ] = "X"  # for eaten iguana
                self.print_grid("end")
                return True
        return False

    def check_win(self):
        """
        Checks if the iguana has reached the goal

        @returns `True` if win, `False` else
        """
        if self.goal == self.iguana_pos:
            self.iguana_escaped = True
            self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "W"  # w for win!
            self.print_grid("end")
            return True

        return False

    def run_round(self, iguana_move, speed=1, do_print=True):
        """Runs a round"""

        # Get the iguana position
        ip = self.iguana_pos
        self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "."  # Clear old iguana pos

        action = None
        if iguana_move == "up":
            action = up
        elif iguana_move == "down":
            action = down
        elif iguana_move == "left":
            action = left
        elif iguana_move == "right":
            action = right

        # do 1 move at a time and test for goal
        ip_1 = action(ip, self.size)
        ip_2 = action(ip_1, self.size)

        self.iguana_pos = ip_1
        if self.check_game_end():
            return

        # optionally draw the grid
        self.print_grid()

        # If the iguana has a speed of 2 then its movement speed is doubled
        if speed == 2:
            self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "."
            self.iguana_pos = ip_2
            if self.check_game_end():
                return

            # optionally draw the grid
            self.print_grid()

        # Now clean the grid of footsteps
        '''for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (self.grid[i][j] == "."):
                    self.grid[i][j] = "-"'''

        self.update_snakes()

    def check_game_end(self):
        # Has the iguana reached the goal
        if self.check_win():
            self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "W"  # w for win!
            return True

        # Has a snake touched the iguana
        elif self.check_loss():
            self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "X"  # for eaten iguana
            return True
        # Nothing happened
        self.grid[self.iguana_pos[1]][self.iguana_pos[0]] = "I"

        return False

    def update_snakes(self):
        # Update the positions of the snakes
        self.snake_positions = []
        for snake in self.snakes:
            self.grid[snake.pos[1]][snake.pos[0]] = "~"  # Slithers
            # print(snake.pos)
            iguana_ded = snake.generate_next_pos(self)
            # print(snake.pos)
            if iguana_ded and snake.pos == self.iguana_pos:
                self.grid[snake.pos[1]][snake.pos[0]] = "X"  # for eaten iguana
                self.iguana_ded = True
            else:
                self.grid[snake.pos[1]][snake.pos[0]] = "S"
                self.snake_positions.append(snake.pos)

        # The snakes have moved
        self.print_grid("s")  # Finally print the updated grid

        # Now clean the grid of slithers
        '''for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (self.grid[i][j] == "~"):
                    self.grid[i][j] = "-"'''

    def print_grid(self, turn="i"):
        """Prints out the grid for the user"""

        # Always update goal to show (unless 'W')
        if (
            self.grid[self.goal[1]][self.goal[0]] != "G"
            and self.grid[self.goal[1]][self.goal[0]] != "W"
        ):
            self.grid[self.goal[1]][self.goal[0]] = "G"

        if self.do_print:
            time.sleep(0.25)  # Comment this out if it's annoying to you

            """
            Print the state of the game
            """

            print("-" * (self.size * 2 + 6))
            # Iguana is in control
            if turn == "i":
                print(" " * (self.size // 2) + "Iguana's Turn!")
            # Snake is in control
            elif turn == "s":
                print(" " * (self.size // 2) + "Snakes' Turn!")
            # The game started
            elif turn == "start":
                print(" " * (self.size // 2) + "Start State")
            # The game ended
            else:
                print(" " * (self.size // 2) + "End State")

            self._print_grid()

    def _print_grid(self):
        # Print the grid header
        print("-" * (self.size * 2 + 6))
        # Print the grid
        for row in self.grid:
            print(" " * 3, end="")
            print(*row)
        # Print the grid footer
        print("-" * (self.size * 2 + 6))


if __name__ == "__main__":
    # Just for me to test some stuff
    my_grid = GridEnvironment()  # 21*21, 5 snakes
    # print(my_grid.size)
    # print(my_grid.center)
    my_grid.run_round("right")
    my_grid.run_round("up")

    # for snake in my_grid.snakes:
    # print(snake.generate_next_pos(my_grid))
