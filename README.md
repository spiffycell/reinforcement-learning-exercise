# Reinforcement Learning Exercise

## Overview

This is a simple RL exercise for me that I've been building from scratch.

This machine learns to perform traversal patterns (either navigating or drawing) on a grid. So, for example, we can teach it how to draw letters!

In this app, we must train our model on `templates/`, and test our model on `Tasks/`


## Training our Model

### High-Level

```
$ ./entrypoint --train templates/draw-an-l.json --strategy min_cost
```

We initialize the code from our `entrypoint` file
We select that we want to `--train` our model on a `Template`
- The Template we have chosen above is `templates/draw-an-l.json`
We assign the machine a Strategy, in this case, it's `min_cost`


### What is a Template?

The Template is a matrix of cost and reward functions
- each 'state' on our 'state space' has its set of cost and reward functions
	- We can think of states of state spaces like tiles on a chess board

#### Why do Templates matter?

When it comes to teaching the machine a Task, we do not want to give it explicit instructions. We instead give it a map of cost and reward functions that _reinforces_ the behavior that we want it to exhibit when prompted.

Depending on the Strategy, the bot will travel along the state space in various ways. 

While it does this, it will log its actions, and label them as the Task performed.

This means, that, when we call on the machine to execute the Task, it will do so having learned how to do it all on its own.

### What is a Strategy?

A Strategy is a simple directing principle that the machine will apply while operating. 

Our two big strategies are `min_cost` and `max_reward`. We mentioned before that each state in the state space has its own set of cost and reward functions. 

If the machine's Strategy is `min_cost`, it will move to the states which have the lowest cost adjacent to its current state. If its Strategy is `max_reward`, it will move to the states which have the highest reward adjacent to its current state.

This way, we don't instruct the machine on what to do, but what its interests are. The Template and the Strategy are paired together to reinforce the desired behavior.

## Testing our model

```
$ ./entrypoint --test tasks/draw-an-l.Task
```

After our training session with the machine is successful, a Task corresponding to our Template will be created in the `tasks/` folder

We can use this `.task` file to test whether or not our training worked.

For `draw-an-l`, the bot will output the coordinates of the states it will travel to in order to form an "L"

It is able to do this, because, in the training session, it logged the actions it took in order to satisfy its Strategy while navigating the Template

So, the `.task` file is simply the bot's "Notes to Self" on what steps to take to navigate that particular Template, given its `min_cost` Strategy


## Closing Thoughts

Thank you for taking the time to read this and explore the code - I hope you find it just as fun to explore as it was for me to learn about and build!

_spiffycell_
