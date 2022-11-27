from Agent import Agent
from geo_utils import directions, get_coords_from_movement
import random


# trivial implementation: 
#   no communication
#   go to a random spot in pattern
class SimplePatternAgent(Agent):
	def __init__(self,id, vertex, pattern=[]):
		super().__init__(id, vertex)
		self.pattern = pattern
		self.destination = random.choice(self.pattern) if len(pattern) else None

	def generate_transition(self,local_vertex_mapping):
		if (self.destination == None or 
				(self.location.x == self.destination[0] and self.location.y == self.destination[1])):
			return self.location.state, self.state, "S"
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
