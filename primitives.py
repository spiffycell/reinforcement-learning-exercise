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


    def choose_strategy(self, strategy): 
        """ Pick a strategy."""
        if strategy == 'min_cost':
            self.strategy = 'cost'
        elif strategy == 'max_reward':
            self.strategy = 'reward'
        else:
            self.strategy = None
        return


    def change_state(self, new_state):
        """ Move to a new spot."""
        # get tranform for new state
        current = np.array(self.current_state.coord)
        action = np.array(new_state["transform"])
        new = list(np.add(action, current))
        logging.info("Moved to space:%s\n", new)
        # move to new state
        self.current_state = State(new[0], new[1])
        return action


    def check_health(self):
        """ Check the health of the agent."""
        if self.health <= 0:
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
            optimal_value = min([adj_space["value"] for adj_space \
                in adjacents])
        elif self.strategy == 'reward':
            optimal_value = max([adj_space["value"] for adj_space \
                in adjacents])

        # get the entry that owns the optimal value
        optimal_entry = next((adj_space for adj_space in adjacents \
                if adj_space["value"] == optimal_value), None)

        logging.info("Optimal entry is:%s\n", optimal_entry)
        return optimal_entry


    def look(self, direction, template):
        """ Get the cost/reward of an adjacent state."""
        # what are the coords my current position?
        current = np.array(self.current_state.coord)
        logging.info("Current position:%s", current)

        # what are the coords of the adjacent position?
        action = np.array(self.transforms[direction])

        # get new position
        new = list(np.add(action, current))
        logging.info("Proposed new position:%s", new)

        # handle out of bounds
        for num in new:
            if num < 0:
                if self.strategy == 'cost':
                    return 100
                elif self.strategy == 'reward':
                    return 0

        # what is the function value of the adjacent position?
        move_value = template.temp_file['template'][new[0]][new[1]][self.strategy]
        logging.info("Corresponding template entry: %s", template.temp_file['template'][new[0]][new[1]])
        return move_value


    def take_cost_reward(self):
        """ Update the health of the agent."""
        self.health -= self.current_state.cost
        self.health += self.current_state.reward


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
