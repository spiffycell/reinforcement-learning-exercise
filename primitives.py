import logging
import numpy as np
import sys


class Agent:
    """ Agent object."""
    def __init__(self, current_state=None):
        """ Initialize Agent object."""
        self.current_state = current_state
        self.strategy = None
        self.transforms = {"up": [1, 0], "down": [-1, 0], \
                "left": [0, -1], "right": [0, 1]} 
        self.health = 100
        return


    def choose_strategy(strategy): 
        """ Pick a strategy."""
        if strategy == 'min_cost':
            self.strategy = 'cost'
        elif strategy == 'max_reward':
            self.strategy = 'reward'
        else:
            self.strategy = None
        return


    def change_state(new_state):
        """ Move to a new spot."""
        # take action

        # move to new state
        self.current_state = new_state
        return action


    def check_health(self):
        """ Check the health of the agent."""
        if self.health >= 0:
            logging.info("The agent has died.")
            sys.exit(1)
        

    def check_adjacents(self, template):
        """ Check adjacent spaces."""
        # what is the cost of moving to a given adjacent space
        adjacents = [{"name": "up", "transform": self.transforms["up"], \
                "value": self.look("up", template)}, \
                {"name": "down", "transform": self.transforms["down"], \
                "value": self.look("down", template)}, \
                {"name": "left", "transform": self.transforms["left"], \
                "value": self.look("left", template)}, \
                {"name": "right", "transform": self.transforms["right"], \
                "value": self.look("right", template)}]

        # get the optimal value
        if self.strategy == 'cost':
            optimal_value = min([adj_space[self.strategy] for adj_space \
                in adjacents])
        elif self.strategy == 'reward':
            optimal_value = max([adj_space[self.strategy] for adj_space \
                in adjacents])

        # get the entry that owns the optimal value
        optimal_entry = next((adj_space for adj_space in adjacents \
                if adj_space[self.strategy] == optimal_value), None)

        return optimal_entry


    def look(self, direction, template):
        """ Get the cost/reward of and adjacent state."""
        # what are the coords my current position?
        current = np.array(self.current_state.coords)

        # what are the coords of the adjacent position?
        new = np.array(self.transforms[direction])
        move = list(np.add(new, current))

        # what is the function value of the adjacent position?
        move_value = template['template'][move[0]][move[1]][self.strategy]

        # get the values
        
        # get the optimal value
        if self.strategy == 'cost':
        # get the min 
        elif self.strategy == 'reward':
        # get the max

        # get the corresponding name of the operation
        # get the corresponding transform to be undertaken

        return move_value


class ActionSpace:
    """ ActionSpace object."""
    def __init__(self):
        """ Initialize ActionSpace object."""
        # the realm of actions which are available to the agent
        # to instantiate our actionspace, we can create an action
        # that inherits its identity from being in the space of actions
        # is the action space an array of actions?
        self.actions = ["up", "down", "left", "right"]
        return


class Action(ActionSpace):
    """ Action object."""
    def __init__(self, name):
        """ Initialize Action object."""
        # the action which the agent is taking
        self.name = name
        return


class StateSpace:
    """ StateSpace object."""
    def __init__(self):
        """ Initialize StateSpace object."""
        # the set of all possible states
        import numpy as np
        self.order = (5, 5)
        self.board = np.empty(self.order)
        return


class State(StateSpace):
    """ State object."""
    def __init__(self, x_coord, y_coord):
        """ Initialize State object."""
        # the state which the agent is currently on
        self.reward = ''
        self.cost = ''
        self.action_set = []

        # declare coordinates
        self.coord = (x_coord, y_coord)
        self.x_coord = x_coord
        self.y_coord = y_coord 
        return


class StrategySpace:
    """ StrategySpace object."""
    def __init__(self):
        """ Initialize StrategySpace object."""
        # the realm of all possible strategies
        return


class Strategy(StrategySpace):
    """ Strategy object."""
    def __init__(self):
        """ Initialize Strategy object."""
        # the strategy the agent is currently employing
        return


class Template:
    """ Template object."""
    def __init__(self):
        """ Initialize template object."""
        self.temp_file = ''
        return

    def load(self, filename):
        """ Load a template from file."""
        import json
        file_data = open(filename, 'r').read()
        self.temp_file = json.loads(file_data)
        return

    def parse(self):
        """ Parse loaded template object."""
        return


class Path():
    """ Path object."""
    def __init__(self):
        """ Initialize path object."""
        # the path the agent is taking
        self.moves = []
        return

    def log_moves(self, action): 
        """ Log move.""" 
        self.moves.append(action)
        return

    def save(self, task):
        """ Save action set in file named after task."""
        with open(f"tasks/{task}.task", "w") as f:
            f.write(self.moves)
        return
