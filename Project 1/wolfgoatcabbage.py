# Has to be changed to 'from search import *' for gradescope. Remove the single quotes.
#from aima.search import *
from search import *


class WolfGoatCabbage(Problem):
    # Initialize class, super() must be included as this class functions as a subclass from Problem
    def __init__(self, initial=frozenset({'W', 'G', 'C', 'F'}), goal=frozenset({})):
        super().__init__(initial,goal)

    # goal_test will return a boolean and check if our current state is ever the goal state
    def goal_test(self, state):
        return state == self.goal
    
    # result will return a new state given the current state and an action
    def result(self, state, action):
        # If farmer is on the left side, remove action from state, if he is on the right side, add action to state
        if "F" in state:
            new_state = state - action
        else:
            new_state = state.union(action)
        new_state = frozenset(new_state)
        return new_state
    
    # Defines all VALID actions in any given state
    def actions(self, state):
        # All POSSIBLE actions as the farmer can either take something with him or go alone
        possible_actions = [{'F'}, {'F', 'G'}, {'F', 'W'}, {'F', 'C'}]

        # Initial State: Only possible option is for the Farmer to take the goat
        if state == {'F', 'G', 'W', 'C'}:
            possible_actions.remove({'F'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F', 'W'})
        # Only possible options are for farmer to take wolf or farmer to take cabbage
        elif state == {'F', 'W', 'C'}:
            possible_actions.remove({'F', 'G'})
            possible_actions.remove({'F'})
        # Only choice is for farmer to take the wolf
        elif state == {'F', 'W', 'G'}:
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F', 'G'})
            possible_actions.remove({'F'})
        # Only choice is for the farmer to take the cabbage
        elif state == {'F', 'G', 'C'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'G'})
            possible_actions.remove({'F'})
        # Only choice is for farmer to bring the goat
        elif state == {'F', 'G'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F'})
        # Only choice is for the farmer to come back
        elif state == {'W', 'C'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F', 'G'})
        # Only choice is for the farmer to bring back the goat
        elif state == {'W'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F'})
        # Farmer should come back by himself
        elif state == {'G'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F', 'G'})
        # Only choice is for the farmer to bring back the goat
        elif state == {'C'}:
            possible_actions.remove({'F', 'W'})
            possible_actions.remove({'F', 'C'})
            possible_actions.remove({'F'})
        return possible_actions


if __name__ == '__main__':
    # Declare class object
    wgc = WolfGoatCabbage()
    # Call depth and breadth first search and print solutions
    solution = depth_first_graph_search(wgc).solution()
    print(solution)
    solution = breadth_first_graph_search(wgc).solution()
    print(solution)
