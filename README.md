# Reinforcement Learning Exercise

This is a simple RL exercise for me that I'm building from scratch.

In this app, we can choose to train the model or to test it.

If we train it:
- we select a Template from the `templates` directory
	- this template is a matrix of cost and reward functions
- the template maps to the state space
- an agent is spawned at a given state in the state space
- the agent is given a strategy. the two main ones:
	- to maximize rewards
	- to minimize costs
		- if the agent's health hits or goes below zero, the agent \
		dies, and the training fails
- for each space the agent is on, it must move to a new one
	- the agent will move to iteratively optimize for its given strategy
	- for each move taken, it will log its action
		- this will create a sequence of actions
- when the agent reaches the destination
	- the complete action sequence is saved and labeled
	- the machine has taught itself the actions needed to take to follow a given task


If we test it:
- we will pull the task from the `task/` folder
- the agent will perform the requested task when prompted
	- labeled action sequence is performed
