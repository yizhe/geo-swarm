from AgentState import AgentState
from geo_utils import directions, get_coords_from_movement
import random

class Agent:
	def __init__(self,id, vertex):
		self.id = id
		self.state = AgentState()
		self.location = vertex

	def generate_transition(self,local_vertex_mapping):
		nearby_agents = []
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				if self != agent:
					nearby_agents.append(agent)
		# Try to spread out
		if len(nearby_agents) == 0:
			return self.location.state, self.state, "S"
		total_dist = 0
		for agent in nearby_agents:
			total_dist += min(abs(self.location.x-agent.location.x), 50-abs(self.location.x-agent.location.x))
			total_dist += min(abs(self.location.y-agent.location.y), 50-abs(self.location.y-agent.location.y))

		best_moves = []
		best_distance = 100000
		for direction in directions:
			new_loc = get_coords_from_movement(self.location.x, self.location.y, direction)
			dist = 0
			for agent in nearby_agents:
				dist += min(abs(new_loc[0]-agent.location.x), 50-abs(new_loc[0]-agent.location.x))+min(abs(new_loc[1]-agent.location.y), 50-abs(new_loc[1]-agent.location.y))
			if dist < best_distance:
				best_distance = dist
				best_moves = [direction]
			if dist == best_distance:
				best_moves.append(direction)
		best_moves.append("S")
		return self.location.state, self.state, random.choice(best_moves)

		# Random direction movement
		# return self.state, direction[randint(0,4)] 


