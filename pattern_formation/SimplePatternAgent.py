from Agent import Agent
from geo_utils import directions, get_coords_from_movement
import random
from constants import INFLUENCE_RADIUS
from copy import deepcopy

# trivial implementation: 
#   no communication
#   go to a random spot in pattern
class SimplePatternAgent(Agent):
	def __init__(self,id, vertex, pattern=[]):
		super().__init__(id, vertex)
		self.pattern = deepcopy(pattern)
		self.finished = False
		self.destination = self.pick_destination()

	def generate_transition(self,local_vertex_mapping):
		# Do nothing when finished
		if (self.destination == None or self.finished == True):
			return self.location.state, self.state, "S"
		dx = self.destination[0] - self.location.x
		dy = self.destination[1] - self.location.y
		# When close to target
		if (abs(dx) <= INFLUENCE_RADIUS and abs(dy) <= INFLUENCE_RADIUS):
			target_vertex = local_vertex_mapping[(dx, dy)] 
			agent_status_at_target = [agent.finished for agent in target_vertex.agents]
			if any(agent_status_at_target):
				self.change_destination()
			# At target
			if (dx == 0 and dy == 0):
				print("Agent ", self.id, "arrives at ", self.destination)
				count = len(target_vertex.agents) 
				if count == 1:
					print("Agent ", self.id, "is done!")
					self.finished = True
					return self.location.state, self.state, "S"
				elif random.random() < 1/count:
					return self.location.state, self.state, "S"
				else:
					return self.location.state, self.state, random.choice(["U", "D", "L", "R"])
		#Move to target
		possible_moves = []
		if self.location.x < self.destination[0]:
			possible_moves.append("R")
		if self.location.x > self.destination[0]:
			possible_moves.append("L")
		if self.location.y < self.destination[1]:
			possible_moves.append("U")
		if self.location.y > self.destination[1]:
			possible_moves.append("D")
		return self.location.state, self.state, random.choice(possible_moves)

	def change_destination(self):
		print("Agent ", self.id, "changes destination from ", self.destination)
		#try:
		self.pattern.remove(self.destination)
		#except ValueError:
		#	print(self.id)
		#	print(self.destination)
		#	print(self.pattern)
		self.destination = self.pick_destination()
		print("Agent ", self.id, "changes destination to ", self.destination)

	def pick_destination(self):
		min_dist = 100000
		estination = None
		for p in self.pattern:
			dist = abs(p[0] - self.location.x) + abs(p[1] - self.location.y)
			if dist < min_dist:
				min_dist = dist
				destination = p
		return destination

