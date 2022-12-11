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
		self.destination = None
		self.pick_destination(self.pattern)

	def generate_transition(self,local_vertex_mapping):
		# Do nothing when finished
		if self.finished == True:
			return self.location.state, self.state, "S"
		# check all destinations
		taken_destination = []
		for p in self.pattern:
			dx = p[0] - self.location.x
			dy = p[1] - self.location.y
			if (abs(dx) <= INFLUENCE_RADIUS and abs(dy) <= INFLUENCE_RADIUS):
				p_vertex = local_vertex_mapping[(dx, dy)] 
				agent_finish_at_p = [agent.finished for agent in p_vertex.agents]
				agent_ids = [agent.id for agent in p_vertex.agents]
				if (len(agent_finish_at_p) > 0 and any(agent_finish_at_p)):
					taken_destination.append(p)
		for taken_p in taken_destination:
			self.pattern.remove(taken_p)
		if (self.destination not in self.pattern):
			self.pick_destination(self.pattern)

		# When at target
		if (self.destination[0] == self.location.x and self.destination[1] == self.location.y ):
			current_vertex = local_vertex_mapping[(0, 0)] 
			print("Agent ", self.id, "arrives at ", self.destination)
			count = len(current_vertex.agents) 
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

	def pick_destination(self, pattern):
		if len(pattern) == 0:
			return
		self.destination = None
		dist_l = [abs(p[0] - self.location.x) + abs(p[1] - self.location.y) for p in pattern]
		weight_l = [1/d for d in dist_l]
		self.destination = random.choices(pattern, weights=weight_l)[0]
		print("Agent ", self.id, "chooses destination to ", self.destination)

