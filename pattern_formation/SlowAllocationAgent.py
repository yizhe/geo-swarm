from Agent import Agent
from geo_utils import directions, get_coords_from_movement
import random
import constants


# trivial implementation: 
#   no communication
#   go to a random spot in pattern
class SlowAllocationAgent(Agent):
	def __init__(self,id, vertex, pattern=[]):
		super().__init__(id, vertex)
		self.pattern = pattern
		self.target = None

	def generate_transition(self,local_vertex_mapping):
		
		all_agents = []
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				all_agents.append(agent)
		dists = []
		ownid = 0
		for idx, agent in enumerate(all_agents):
			if agent == self:
				ownid = idx
			for id, i in enumerate(self.pattern):
				d = abs(agent.location.x-i[0]) + abs(agent.location.y-i[1])
				dists.append((d, idx, id))
		dists = sorted(dists)
		assigned = {}
		occupied = {}
		for i in dists:
			if i[1] not in assigned.keys() and i[2] not in occupied.keys():
				occupied[i[2]] = i[1]
				assigned[i[1]] = i[2]
		self.target = self.pattern[assigned[ownid]]
		
		best_move = None
		best_distance = 100000
		for direction in directions:
			i = get_coords_from_movement(self.location.x, self.location.y, direction)
			dist = abs(self.target[0]-i[0])+abs(self.target[1]-i[1])
			if dist < best_distance:
				best_distance = dist
				best_move = direction
		#best_moves.append("S")
		return self.location.state, self.state, best_move
