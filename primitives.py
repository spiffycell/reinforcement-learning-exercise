import logging
import numpy as np
import sys


class Agent:
    """ Agent object."""
    def __init__(self, current_state=None):
        """ Initialize Agent object."""
        self.current_state = current_state
        self.previous_state = current_state
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
        logging.debug("Moved to space:%s\n", new)
        # move to new state
        self.previous_state = self.current_state
        self.current_state = State(new[0], new[1])
        self.current_state.cost = new_state["cost"]
        self.current_state.reward = new_state["reward"]
        return action


    def check_health(self):
        """ Check the health of the agent."""
        if self.health <= 0:
            logging.debug("The agent has died.")
            sys.exit(1)
        

    def check_adjacents(self, template):
        """ Check adjacent spaces."""
        # what is the cost/reward of moving to a given adjacent space
        adjacents = [{"name": "up", "transform": self.transforms["up"], \
                "cost": self.look("up", template, value="cost"), \
                "reward": self.look("up", template, value="reward")}, \
                {"name": "down", "transform": self.transforms["down"], \
                "cost": self.look("down", template, value="cost"), \
                "reward": self.look("down", template, value="reward")}, \
                {"name": "left", "transform": self.transforms["left"], \
                "cost": self.look("left", template, value="cost"), \
                "reward": self.look("left", template, value="reward")}, \
                {"name": "right", "transform": self.transforms["right"], \
                "cost": self.look("right", template, value="cost"), \
                "reward": self.look("right", template, value="reward")}]

        # show adjacents
        logging.debug("List of adjacents: %s\n", adjacents)

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

        logging.debug("Optimal entry is:%s\n", optimal_entry)
        return optimal_entry


    def look(self, direction, template, value=None):
        """ Get the cost/reward of an adjacent state."""
        # what are the coords my current position?
        current = np.array(self.current_state.coord)
        logging.debug("Current position:%s", current)

        # what are the coords of the adjacent position?
        action = np.array(self.transforms[direction])

        # get new position
        new = list(np.add(action, current))
        logging.debug("Proposed new position:%s", new)

        # RULE: no out of bounds
        for num in new:
            if num < 0 or num > 4:
                pp_val = self.poison_pill(value)
                return pp_val

        # RULE: no revisiting prior states
        if new == self.previous_state.coord:
            pp_val = self.poison_pill(value)
            return pp_val

        # what is the function value of the adjacent position?
        move = template.temp_file['template'][new[0]][new[1]][self.strategy]
        logging.debug("Corresponding template entry: %s", template.temp_file['template'][new[0]][new[1]])
        return move


    def poison_pill(self, value):
        """ Make a possible state change unappealing."""
        if value == 'cost':
            if self.strategy == 'cost':
                return 100
            elif self.strategy == 'reward':
                return 0
        elif value == 'reward':
            if self.strategy == 'cost':
                return 100
            elif self.strategy == 'reward':
                return 0


    def take_cost_reward(self):
        """ Update the health of the agent."""
        # we need to get both cost and reward
        self.health -= self.current_state.cost
        self.health += self.current_state.reward


class Action:
    """ Action object."""
    def __init__(self, current_state=None):
        """ Initialize Actions object."""
        self.actions = {"up": [1, 0], "down": [-1, 0], \
                "left": [0, -1], "right": [0, 1]} 
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
        self.reward = None 
        self.cost = None 
        self.action_set = []

        # declare coordinates
        self.coord = [x_coord, y_coord]
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
            f.write(str(self.moves))
        return
