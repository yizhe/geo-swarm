import random 
from collections import namedtuple

AgentTransition = namedtuple("AgentTransition", "state direction")
LocalTransitory = namedtuple("LocalTransitory", "vertex_state, agent_updates")

def naive_resolution(proposed_vertex_states, proposed_agent_updates):
	return LocalTransitory(list(proposed_vertex_states.values())[0], proposed_agent_updates)

def winner_takes_all(proposed_vertex_states, proposed_agent_updates):
	agents = proposed_vertex_states.keys()
	winner = random.choice(agents)
	new_vertex_state = proposed_vertex_states[winner]
	new_agent_updates = {}
	for agent in proposed_agent_updates.keys():
		if agent == winner:
			new_agent_updates[agent] = proposed_agent_updates[agent]
		else:
			new_agent_updates[agent] = None
