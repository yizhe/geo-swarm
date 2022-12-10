from Agent import Agent
from geo_utils import directions, get_coords_from_movement
import random


# trivial implementation: 
#   no communication
#   go to a random spot in pattern
class AllocationAgent(Agent):
	def __init__(self,id, vertex, pattern=[]):
		super().__init__(id, vertex)
		self.pattern = pattern
		self.target = None
		self.taken = {}
		self.finished = 0

	def check_conflict(self, msg):
		for i in self.msgs:
			if i[1] == msg[1] and i[0] < msg[0]:
				return True
		return False

	def generate_transition(self,local_vertex_mapping):
		nearby_agents = []
		ownid = 0
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				nearby_agents.append(agent)
				if self == agent:
					ownid = len(nearby_agents)-1
		dists = []
		occupied = {}
		assigned = {}
		for id, i in enumerate(self.pattern):
			if id in occupied.keys() or id in self.taken.keys():
				continue
			for idx, agent in enumerate(nearby_agents):
				if idx in assigned.keys():
					continue
				if agent.finished:
					self.taken[agent.finished] = True
					continue
				d = abs(agent.location.x-i[0]) + abs(agent.location.y-i[1])
				if d == 0:
					occupied[id] = idx
					assigned[idx] = id
					self.taken[id] = True
					if idx == ownid:
						self.finished = id
					break
		if self.finished:
			return self.location.state, self.state, None
		for id, i in enumerate(self.pattern):
			if (id in occupied.keys()) or (id in self.taken.keys()):
				continue
			for idx, agent in enumerate(nearby_agents):
				if idx in assigned.keys() or agent.finished:
					continue
				d = abs(agent.location.x-i[0]) + abs(agent.location.y-i[1])
				dists.append((d, id, idx, i[0], i[1]))

		dists = sorted(dists)

		for i in dists:
			if (i[1] not in occupied.keys()) and (i[2] not in assigned.keys()):
				occupied[i[1]] = i[2]
				assigned[i[2]] = i[1]
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
