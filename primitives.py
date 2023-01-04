import ast
import json
import logging
import numpy as np
import sys


class Policy():
    """ Policy object."""
    def __init__(self, name):
        """ Initialize policy object."""
        # the path the agent is taking
        self.short_name = None
        self.name = name 

        # store short_name
        if self.name == 'min_cost':
            self.short_name = 'cost'
        elif self.name == 'max_reward':
            self.short_name = 'reward'
        return

    def apply(self, adjacents):
        if self.name == 'min_cost':
            optimal_value = min([adj_space[self.short_name] for adj_space \
                in adjacents])
        elif self.name == 'max_reward':
            optimal_value = max([adj_space[self.short_name] for adj_space \
                in adjacents])

        return optimal_value


class Agent:
    """ Agent object."""
    def __init__(self, current_state=None):
        """ Initialize Agent object."""
        self.current_state = current_state
        self.previous_state = current_state
        self.policy = None
        self.transforms = {"up": [1, 0], "down": [-1, 0], \
                "left": [0, -1], "right": [0, 1]} 
        self.traversal = []
        self.health = 100
        return

    def choose_policy(self, policy_name): 
        """ Pick a strategy."""
        self.policy = Policy(policy_name)
        return

    def change_state(self, new_state, mode=None):
        """ Move to a new spot."""
        # get current state
        current = np.array(self.current_state.coord)
        # get transform
        action = np.array(new_state["transform"])

        # calculate the new state
        new = list(np.add(action, current))
        logging.info("Moved to space:%s", new)

        # move to new state
        self.previous_state = self.current_state
        self.current_state = State(new[0], new[1])

        # set the cost and reward values for agent health update
        if mode == "train": 
            self.current_state.cost = new_state["cost"]
            self.current_state.reward = new_state["reward"]
        elif mode == "test":
            self.traversal.append(current_state.coord)
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
        optimal_value = self.policy.apply(adjacents)

        # get the entry that owns the optimal value
        optimal_entry = next((adj_space for adj_space in adjacents \
                if adj_space[self.policy] == optimal_value), None)

        logging.debug("Optimal entry is:%s\n", optimal_entry)
        return optimal_entry

    def look(self, direction, strategy, value=None):
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
            # future consideration: what if the grid is not square?
            # how to handle out-of-bounds conditions (both rows and cols)?
            if num < 0 or num > (strategy.rows - 1):
                pp_val = self.poison_pill(value)
                return pp_val

        # RULE: no revisiting prior states
        if new == self.previous_state.coord:
            pp_val = self.poison_pill(value)
            return pp_val

        # what is the function value of the adjacent position?
        move = strategy.temp_file['strategy'][new[0]][new[1]][self.policy]
        logging.debug("Corresponding strategy entry: %s", strategy.temp_file['strategy'][new[0]][new[1]])
        return move

    def poison_pill(self, value):
        """ Make a possible state change unappealing."""
        if value == 'cost':
            if self.policy == 'cost':
                return 100
            elif self.policy == 'reward':
                return 0
        elif value == 'reward':
            if self.policy == 'cost':
                return 100
            elif self.policy == 'reward':
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


class Task:
    """ Task object."""
    def __init__(self):
        """ Initialize task object."""
        self.task_data = ''
        return

    def load(self, filename):
        """ Load a task from file."""
        file_data = open(filename, 'r').read()
        self.task_data = ast.literal_eval(file_data)
        return

    def parse(self):
        """ Parse task file data."""
        return


class Strategy:
    """ Strategy object."""
    def __init__(self):
        """ Initialize strategy object."""
        self.temp_file = ''
        self.temp_rows = ''
        self.temp_cols = ''
        return

    def load(self, filename):
        """ Load a strategy from file."""
        task_data = open(filename, 'r').read()
        self.temp_file = json.loads(task_data)
        self.rows = len(self.temp_file["strategy"]) 
        self.cols = len(self.temp_file["strategy"][0]) 
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
        # do we want to reformat before storing?
        action_obj = {"transform": list(action)}
        self.moves.append(action_obj)
        logging.info("Storing action: %s", action_obj)
        return

    def save(self, task):
        """ Save action set in file named after task."""
        # create the full dictionary object
        move_sequence = {}
        move_sequence["task"] = self.moves

        # and export it
        with open(f"tasks/{task}.task", "w") as f:
            f.write(str(move_sequence))
        return


class Policy():
    """ Policy object."""
    def __init__(self, name):
        """ Initialize policy object."""
        # the path the agent is taking
        self.name = name 
        return
