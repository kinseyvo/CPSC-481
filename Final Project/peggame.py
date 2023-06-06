import search
from search import *
import turtle as T
import time

# Set the radius of the pegs (drawn as simple circles) as well as their positions within the triangle board
peg_radius = 30

# This array of tuples is our coordinate system for the pegs, arranged as a triangle. Index 0 is Peg0, index1
# is Peg2 and so on.
pegs = [(0, 200), (-75, 100), (75, 100), (-125, 0), (0, 0), (125, 0), (-200, -115), (-75, -115), (75, -115),
        (200, -115), (-250, -225), (-125, -225), (0, -225), (125, -225), (250, -225)]


# Class turtle window is a singleton class, which allows us to use the same turtle window in every method or function
# in our program
class TurtleWindow:
    # Initialize instance to None
    instance = None

    # getInstance will check if a turtle window has been created anywhere in the program, if it has ALREADY been created
    # it will return the already created instance instead of creating a new one. If it has NOT been created, only then
    # will it create a new instance
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = TurtleWindow()
        return cls.instance

    # The constructor of TurtleWindow is responsible for setting up the initial state of our board and the pegs
    def __init__(self):
        # Initialize our screen
        self.screen = T.Screen()

        self.delay = 0.25

        # Setting our screen size of 800x800 to fit most displays
        self.screen.setup(width=800, height=800)

        # Set the screen background color to white for readability
        self.screen.bgcolor("white")

        # Screen Title
        self.screen.title("Peg Game")

        # Initialize our pen to draw shapes. Set up speed and pen size for readability
        self.pen = T.Turtle()
        self.pen.speed("fastest")
        self.pen.pensize(5)

    # get_index_from_coord takes a coordinate (i1, j1), which corresponds to a specific action on the board. For
    # example, if we pass in (2, 1) then we want the peg at row 3 position 2 (accounting for zero indexing). Then
    # we can get the valid peg location using these if statements. Note that a valid peg location is a single integer,
    # which corresponds to our pegs[] array
    def get_index_from_coord(self, coord):
        r, c = coord
        # since row is 0, we know it can only be index 0
        if r == 0:
            return 0
        # if the row is 1, then we can add the column value to get our index of 1 or 2
        if r == 1:
            return c + r
        # if the row is 2, then we add whatever the column value is plus 3 for an index of 3, 4, or 5
        if r == 2:
            return c + 3
        # if the row is 3, then we add whatever the column value is plus 6 for an index of 6, 7, 8, or 9
        if r == 3:
            return c + 6
        # if the row is 4, then we add whatever the column value is plus 6 for an index of 10, 11, 12, 13, or 14
        if r == 4:
            return c + 10

    # This function is specifically for changing the state (color) of a single peg
    def change_peg_color(self, coord, peg_color):
        # By calling this method, we get a specific peg index for a given coordinate. For example, (2, 0) will give us
        # an index of 3
        peg_number = self.get_index_from_coord(coord)
        self.pen.penup()
        self.pen.goto(pegs[peg_number])
        self.pen.pendown()
        self.pen.fillcolor(peg_color)
        self.pen.begin_fill()
        self.pen.circle(30)
        self.pen.end_fill()
        time.sleep(0.25)

    # get_colors is a helper function used in the draw() method. It gives us our list of colors when we are drawing the
    # pegs
    def get_colors(self, state):
        colors = []
        for row in state:
            colors.extend(row)

        return colors

    # draw() does exactly what you think it does. Given a state it will draw it's representation using the turtle module
    def draw(self, state):
        # Pen will be moved to initial position to draw the board
        self.pen.penup()
        self.pen.goto(-350, -250)
        self.pen.pendown()

        colors = self.get_colors(state)
        # Loop to draw a triangle to fit within the allotted screen.
        for x in range(3):
            # Draw for 700 pixels and then rotate 120 degrees 3 times to form a triangle
            self.pen.forward(700)
            self.pen.left(120)

        # This list is a set of colors to represent the state of the pegs. Blue means occupied, red means jump-able,
        # black means empty.
        color_set = ['white', 'blue', 'red']

        # Using the coordinates of the pegs, go to each position and draw a circle with a given filled in color
        for c, v in enumerate(pegs):
            self.pen.penup()
            self.pen.goto(v)
            self.pen.pendown()
            self.pen.fillcolor(color_set[colors[c]])
            self.pen.begin_fill()
            self.pen.circle(peg_radius)
            self.pen.end_fill()

        # Hiding the turtle for readability and ensuring the program continues until the user exits
        self.pen.hideturtle()

    # This is a helper function, it finds the turtle instance and deletes all allocated resources after the user exits
    # the window
    def close_window(self):
        T.bye()

    # animate() game takes a list of states and actions from the final game state and uses the turtle module to show
    # the chosen pegs for each move from initial state to goal state
    def animate_game(self, states, actions):
        # zip allows us to combine a relevant state with its given action
        for state, action in zip(states, actions):
            # Check if not None first to account for the initial state having no related action
            if action is not None:
                # Action is grouped up into a source tuple and a destination tuple, break them up here
                src, dst = action
                # Now with the src and dst, we can change the peg colors to highlight which peg is the source and which
                # is the destination
                self.change_peg_color(src, "red")
                self.change_peg_color(dst, "green")
                time.sleep(self.delay)

            # Make sure to draw the new state after each new state
            self.draw(state)


# Class PegGame will accept an initial state and a boolean to check if the user wants to draw the state or not
class PegGame(Problem):
    def __init__(self, initial=((0,), (1, 1), (1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1, 1)), draw=False):
        super().__init__(initial)
        self.draw = draw
        # Only if draw is True will we get the instance and draw the initial board
        if self.draw:
            initial_window = TurtleWindow.getInstance()
            initial_window.draw(self.initial)

    # goal_test will return a boolean and check if our current state is ever the goal state
    def goal_test(self, state):
        is_goal = 0
        # loop through the game board and check if ONLY ONE peg is 1 and the rest are zero. This means that only one
        # peg is remaining in the board and all the rest are empty, which is the goal state
        for row in state:
            for peg in row:
                if peg == 1:
                    is_goal += 1
        return is_goal == 1

    # result will return a new state given the current state and an action
    def result(self, state, action):
        # Remember, actions is a tuple of tuples so we need to split it up.
        (i1, j1), (i2, j2) = action

        # Our state that's passed in needs to be a sorted list so we can modify the elements. This will allow us to
        # remove the pegs that have been selected and jumped over and to fill empty pegs
        new_state = [list(row) for row in sorted(state, key=len)]

        # There is an if statement here because it has to check if draw is True or False in main. It will only draw the
        # board if it's true.
        if self.draw:
            turtle_window = TurtleWindow.getInstance()
            turtle_window.change_peg_color((i1, j1), "red")

        # starting peg is set to zero because we are "lifting" our chosen peg
        new_state[i1][j1] = 0

        # middle peg is zero because we are "jumping" over this peg with our starting peg. Both the starting peg and the
        # middle peg will be set to zero
        new_state[(i1 + i2) // 2][(j1 + j2) // 2] = 0

        # ending peg (assuming the action is valid) starts as empty which is zero, so now we set it to one since we are
        # moving our starting peg into this ending peg like checkers
        new_state[i2][j2] = 1

        # Convert our new_state back to a tuple of tuples, using map ensures that we preserve the order during
        # conversion
        new_state = tuple(map(tuple, new_state))

        # There is an if statement here because it has to check if draw is True or False in main. It will only draw the
        # board if it's true.
        if self.draw:
            turtle_window = TurtleWindow.getInstance()
            turtle_window.change_peg_color((i2, j2), "green")
            turtle_window.draw(new_state)

        return new_state

    # actions() represents our logic at any given point in the game. This is very dense, and details at every state the
    # valid moves that are associated with a given peg location
    def actions(self, state):
        valid_actions = []
        # Convert state to a list of lists
        state_as_list = sorted(list(state), key=lambda t: len(t))

        # This for loop will go through the entire game board from start to finish. It is a two dimensional for loop to
        # account for the rows and columns of the board
        for row_index, row in enumerate(state_as_list):
            for col_index, peg in enumerate(row):
                # This makes sure that it will only calculate valid actions only if the peg is actually empty, or zero.
                if peg == 0:
                    # If the length of the row is 1, these are the valid actions, and so on
                    if len(row) == 1:
                        left_middle_peg = (row_index + 1, row_index)
                        left_jumping_peg = (row_index + 2, row_index)

                        right_middle_peg = (row_index + 1, row_index + 1)
                        right_jumping_peg = (row_index + 2, row_index + 2)

                        # # checks if middle peg is filled (1 = has a peg and 0 = is empty)
                        if state_as_list[left_middle_peg[0]][left_middle_peg[1]] == 1 and \
                                state_as_list[left_jumping_peg[0]][left_jumping_peg[1]] == 1:
                            valid_actions.append((left_jumping_peg, (row_index, col_index)))

                        if state_as_list[right_middle_peg[0]][right_middle_peg[1]] == 1 and \
                                state_as_list[right_jumping_peg[0]][right_jumping_peg[1]] == 1:
                            valid_actions.append((right_jumping_peg, (row_index, col_index)))
                    # If we are on row 2, then we can only move down diagonally to the right or to the left
                    if len(row) == 2:
                        left_jumping_peg = (row_index + 2, col_index)
                        if state_as_list[left_jumping_peg[0]][left_jumping_peg[1]] == 1 and \
                                state_as_list[row_index + 1][col_index] == 1:
                            valid_actions.append((left_jumping_peg, (row_index, col_index)))

                        right_jump_peg = (row_index + 2, col_index + 2)
                        if state_as_list[right_jump_peg[0]][right_jump_peg[1]] == 1 and \
                                state_as_list[row_index + 1][col_index + 1] == 1:
                            valid_actions.append((right_jump_peg, (row_index, col_index)))

                    # Here it gets interesting, if we are on row three we need to account for upwards diagonal, downward
                    # diagonal, and left and right horizontally
                    if len(row) == 3:
                        # Checking which peg we are on using the column index allows us to curate our logic to that
                        # specific peg location (for example, we don't need to account for left horizontal jumps if we
                        # are at col_index == 0, since that is the leftmost peg in row 3)
                        if col_index == 0:
                            left_up_jumping_peg = (row_index - 2, col_index)
                            if state_as_list[left_up_jumping_peg[0]][left_up_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index] == 1:
                                valid_actions.append((left_up_jumping_peg, (row_index, col_index)))

                            horizontal_jump_peg = (row_index, col_index + 2)
                            if state_as_list[horizontal_jump_peg[0]][horizontal_jump_peg[1]] == 1 and \
                                    state_as_list[row_index][col_index + 1] == 1:
                                valid_actions.append((horizontal_jump_peg, (row_index, col_index)))

                            down_left_jumping_peg = (row_index + 2, col_index)
                            if state_as_list[down_left_jumping_peg[0]][down_left_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index] == 1:
                                valid_actions.append((down_left_jumping_peg, (row_index, col_index)))

                            down_right_jumping_peg = (row_index + 2, col_index + 2)
                            if state_as_list[down_right_jumping_peg[0]][down_right_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index + 1] == 1:
                                valid_actions.append((down_right_jumping_peg, (row_index, col_index)))

                        # To account for the middle col_index, we now need left and right horizontal jumps as well as
                        # left and right diagonal jumps for both upward and downward
                        if col_index == 1:
                            down_left_jumping_peg = (row_index + 2, col_index)
                            if state_as_list[down_left_jumping_peg[0]][down_left_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index] == 1:
                                valid_actions.append((down_left_jumping_peg, (row_index, col_index)))

                            down_right_jumping_peg = (row_index + 2, col_index + 2)
                            if state_as_list[down_right_jumping_peg[0]][down_right_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index + 1] == 1:
                                valid_actions.append((down_right_jumping_peg, (row_index, col_index)))

                        # To account for the right col_index, we now need only a left horizontal jump as well as
                        # left and right diagonal jumps downward jumps. We only need a left diagonal upward jump here
                        # because we would go out of bounds using a right upward jump
                        if col_index == 2:
                            left_up_jumping_peg = (row_index - 2, col_index - 2)
                            if state_as_list[left_up_jumping_peg[0]][left_up_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index - 1] == 1:
                                valid_actions.append((left_up_jumping_peg, (row_index, col_index)))

                            horizontal_jump_peg = (row_index, col_index - 2)
                            if state_as_list[horizontal_jump_peg[0]][horizontal_jump_peg[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((horizontal_jump_peg, (row_index, col_index)))

                            down_left_jumping_peg = (row_index + 2, col_index)
                            if state_as_list[down_left_jumping_peg[0]][down_left_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index] == 1:
                                valid_actions.append((down_left_jumping_peg, (row_index, col_index)))

                            down_right_jumping_peg = (row_index + 2, col_index + 2)
                            if state_as_list[down_right_jumping_peg[0]][down_right_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index + 1][col_index + 1] == 1:
                                valid_actions.append((down_right_jumping_peg, (row_index, col_index)))

                    if len(row) == 4:
                        if col_index == 0 or col_index == 1:
                            # horizontal jumps
                            right_horizontal_jumping_peg = (row_index, col_index + 2)
                            if state_as_list[right_horizontal_jumping_peg[0]][right_horizontal_jumping_peg[1]] == 1 \
                                    and state_as_list[row_index][col_index + 1] == 1:
                                valid_actions.append((right_horizontal_jumping_peg, (row_index, col_index)))

                            # diagonal jumps
                            left_diagonal_jump_peg = (row_index - 2, col_index)
                            if state_as_list[left_diagonal_jump_peg[0]][left_diagonal_jump_peg[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index] == 1:
                                valid_actions.append((left_diagonal_jump_peg, (row_index, col_index)))

                        if col_index == 2 or col_index == 3:
                            # horizontal jumps
                            left_horizontal_jumping_peg = (row_index, col_index - 2)
                            if state_as_list[left_horizontal_jumping_peg[0]][left_horizontal_jumping_peg[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((left_horizontal_jumping_peg, (row_index, col_index)))

                            # diagonal jumps
                            right_diagonal_jump_peg = (row_index - 2, col_index - 2)
                            if state_as_list[right_diagonal_jump_peg[0]][right_diagonal_jump_peg[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((right_diagonal_jump_peg, (row_index, col_index)))

                    if len(row) == 5:
                        if col_index == 0:
                            # Diagonal
                            zero_idx = (row_index - 2, col_index)
                            if state_as_list[zero_idx[0]][zero_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index] == 1:
                                valid_actions.append((zero_idx, (row_index, col_index)))

                            # Horizontal
                            zero_idx = (row_index, col_index + 2)
                            if state_as_list[zero_idx[0]][zero_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index + 1] == 1:
                                valid_actions.append((zero_idx, (row_index, col_index)))

                        if col_index == 1:
                            # Diagonal
                            one_idx = (row_index - 2, col_index)
                            if state_as_list[one_idx[0]][one_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index] == 1:
                                valid_actions.append((one_idx, (row_index, col_index)))

                            # Horizontal
                            one_idx = (row_index, col_index + 2)
                            if state_as_list[one_idx[0]][one_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index + 1] == 1:
                                valid_actions.append((one_idx, (row_index, col_index)))

                        if col_index == 2:
                            # Diagonal
                            two_idx = (row_index - 2, col_index - 2)  # jumps to the top left
                            if state_as_list[two_idx[0]][two_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index - 1] == 1:
                                valid_actions.append((two_idx, (row_index, col_index)))

                            two_idx = (row_index - 2, col_index)  # jumps to the top right
                            if state_as_list[two_idx[0]][two_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index] == 1:
                                valid_actions.append((two_idx, (row_index, col_index)))

                            # Horizontal
                            two_idx = (row_index, col_index - 2)  # left horizontal peg
                            if state_as_list[two_idx[0]][two_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((two_idx, (row_index, col_index)))

                            two_idx = (row_index, col_index + 2)  # right horizontal peg
                            if state_as_list[two_idx[0]][two_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index + 1] == 1:
                                valid_actions.append((two_idx, (row_index, col_index)))

                        if col_index == 3:
                            # Diagonal
                            three_idx = (row_index - 2, col_index - 2)
                            if state_as_list[three_idx[0]][three_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index - 1] == 1:
                                valid_actions.append((three_idx, (row_index, col_index)))

                            # Horizontal
                            three_idx = (row_index, col_index - 2)
                            if state_as_list[three_idx[0]][three_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((three_idx, (row_index, col_index)))

                        if col_index == 4:
                            # Diagonal
                            four_idx = (row_index - 2, col_index - 2)
                            if state_as_list[four_idx[0]][four_idx[1]] == 1 and \
                                    state_as_list[row_index - 1][col_index - 1] == 1:
                                valid_actions.append((four_idx, (row_index, col_index)))
                            # Horizontal
                            four_idx = (row_index, col_index - 2)
                            if state_as_list[four_idx[0]][four_idx[1]] == 1 and \
                                    state_as_list[row_index][col_index - 1] == 1:
                                valid_actions.append((four_idx, (row_index, col_index)))

        return valid_actions

    def h_demo(self, node):
        return node.depth

    # Help from ChatGPT was used to for help in looping through the filled and
    # open pegs. Function h() relies on the manhattan distance for our heuristic. We chose this because the manhattan
    # distance allows the algorithm to reliably estimate the distance between a peg and an empty hole. This means the
    # algorithm will be more selective to moves that remove pegs more quickly. It is also an admissible heuristic,
    # because it never overestimates the true cost since it doesn't take into account if there is a peg in between the
    # target empty peg and the peg it wants to take
    def h(self, node):
        """ Return the heuristic value for a given state """
        # Set our lists for filled pegs and open pegs, this will be useful in calculating the manhattan distance
        filled_pegs, open_pegs = [], []
        total_score = 0

        # Now, using node.state which is borrowing from class Node in search.py, loop through the rows and columns in
        # node.state and check at each peg location if it is a zero(empty) or a one(filled) and add them to filled_pegs
        # and open_pegs respectively.
        for row_index, row in enumerate(node.state):
            for col_index, peg in enumerate(row):
                if peg == 1:
                    filled_pegs.append((row_index, col_index))
                else:
                    open_pegs.append((row_index, col_index))
        # Attach a negative value to the length of open pegs at each state. Remember, lower scores mean a better
        # heuristic, so more empty pegs in a state means a more favorable move!
        total_score -= (len(open_pegs))

        valid_actions = [src for src, dst in self.actions(node.state)]

        # valid_actions = []
        # for src, dst in self.valid_actions(node.state):
        #     valid_actions.append(src)

        for peg in filled_pegs:
            if peg not in valid_actions:
                total_score += 1

        return total_score

    # This is a helper function for output. It will produce a list from the initial state to the goal state. This
    # represents the algorithm's MOST OPTIMAL path from start to finish
    def trace_solution(self, node):
        game_path = []
        while node:
            game_path.append(node.state)
            node = node.parent
        return list(reversed(game_path))

    # This is a helper function for output. It will produce a list from the initial state to the goal state. This
    # represents the algorithm's MOST OPTIMAL PATH OF ACTIONS path from start to finish
    def trace_actions(self, node):
        game_path = []
        while node:
            game_path.append(node.action)
            node = node.parent
        return list(reversed(game_path))


if __name__ == '__main__':
    peg_game = PegGame(draw=False)
    peg_game_actions = PegGame(draw=True)
    heuristic_zero = PegGame(draw=False)
    running = True
    while running:
        user_input = input("\nPlease enter a demo choice, enter 0 to exit...\n"
                           "1 - Result  Demo\n"
                           "2 - Actions Demo\n"
                           "3 - Full Demo with Heuristic of Zero\n"
                           "4 - Full A* Demo with Optimized Heuristic\n"
                           "What is your choice (input an integer between 1 and 4)? ", )

        user_input = int(user_input)

        if user_input == 0:
            running = False
            window = TurtleWindow.getInstance()
            window.close_window()
        elif user_input == 1:
            peg_game_actions.result(((0,), (1, 1), (0, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1, 1)), ((2, 0), (0, 0)))
        elif user_input == 2:
            window = TurtleWindow.getInstance()
            state = ((1,), (1, 1), (1, 1, 0), (1, 1, 1, 1), (1, 1, 1, 1, 1))
            window.draw(state)
            actions = peg_game_actions.actions(state)
            time.sleep(10)
            for src, dst in actions:
                window.change_peg_color(src, "yellow")
        elif user_input == 3:
            start_time = time.time()
            result = search.best_first_graph_search(heuristic_zero, heuristic_zero.h_demo, display=True)
            end_time = time.time()

            elapsed_time = end_time - start_time

            print(f"Total elapsed time: {elapsed_time:.2f} seconds.\n")

            complete_path = heuristic_zero.trace_solution(result)

            action_path = heuristic_zero.trace_actions(result)

            for i, a in zip(complete_path, action_path):
                print(i, a)
                print('\n')

        elif user_input == 4:
            start_time = time.time()
            result = search.astar_search(peg_game, peg_game.h, display=True)
            end_time = time.time()

            elapsed_time = end_time - start_time

            print(f"Total elapsed time: {elapsed_time:.4f} seconds.\n")

            complete_path = peg_game.trace_solution(result)

            action_path = peg_game.trace_actions(result)

            for i, a in zip(complete_path, action_path):
                print(i, a)
                print('\n')

            TurtleWindow.getInstance().animate_game(complete_path, action_path)
        else:
            print("\nINVALID SELECTION! Please enter an integer between 1 and 4!!")
