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
		self.msgs = []

	def broadcast(self, msg):
		#TODO: broadcasts msg (tuple of target distance and target id) to surrounding neighbors
		pass

	def check_conflict(self, msg):
		for i in self.msgs:
			if i[1] == msg[1] and i[0] < msg[0]:
				return True
		return False

	def generate_transition(self,local_vertex_mapping):
		nearby_agents = []
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				if self != agent:
					nearby_agents.append(agent)
		dists = []
		for id, i in enumerate(self.pattern):
			d = min(abs(self.location.x-i.location.x), 50-abs(self.location.x-i.location.x))
			d += min(abs(self.location.y-i.location.y), 50-abs(self.location.y-i.location.y))
			dists.append((d, id))
		dists = sorted(dists)
		now = -1
		self.target = None
		while self.target is None:
			now = now + 1
			if now >= len(dists):
				raise IndexError
			self.broadcast(dists[now])	
			if not self.check_conflict(dists[now]):
				self.target = self.pattern[dists[now][1]]
		
		best_moves = []
		best_distance = 100000
		for direction in directions:
			i = get_coords_from_movement(self.location.x, self.location.y, direction)
			dist = min(abs(self.target.location.x-i.location.x), 50-abs(self.target.location.x-i.location.x))
			dist += min(abs(self.target.location.y-i.location.y), 50-abs(self.target.location.y-i.location.y))
			if dist < best_distance:
				best_distance = dist
				best_moves = [direction]
			if dist == best_distance:
				best_moves.append(direction)
		#best_moves.append("S")
		return self.location.state, self.state, random.choice(best_moves)
