import logging
import sys

class Agent:
    """ Agent object."""
    def __init__(self, current_state=None):
        """ Initialize Agent object."""
        self.current_state = current_state
        self.strategy = None
        self.health = 100
        return

    def choose_strategy(strategy): 
        """ Pick a strategy."""
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
        
    def check_adjacents(self):
        """ Check adjacent spaces."""
        # what is the cost of moving up
        up = self.look_up()
        down = self.look_down()
        left = self.look_left()
        right = self.look_right()
        return


    def look_up(self):
        """ Get the cost/reward of the tile one up."""
        # what are the coords my current position?
        # what are the coords of the position one up?
        # what is the cost function of the position one up on the template?
        return


    def look_down(self):
        """ Get the cost/reward of the tile one down."""
        # what are the coords my current position?
        # what are the coords of the position one down?
        # what is the cost function of the position one down on the template?
        return


    def look_left(self):
        """ Get the cost/reward of the tile one left."""
        # what are the coords my current position?
        # what are the coords of the position one left?
        # what is the cost function of the position one left on the template?
        return


    def look_right(self):
        """ Get the cost/reward of the tile one right."""
        # what are the coords my current position?
        # what are the coords of the position one right?
        # what is the cost function of the position one right on the template?
        return


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
