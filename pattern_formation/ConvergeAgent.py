from Agent import Agent
from geo_utils import directions, get_coords_from_movement
import random
from constants import INFLUENCE_RADIUS
from copy import deepcopy

# trivial implementation: 
#   no communication
#   no global coordinate
#   coordinates have same orientation

class ConvergeAgent(Agent):
	def __init__(self,id, vertex, pattern=[]):
		super().__init__(id, vertex)
		pattern_min_x = min(p[0] for p in pattern)
		pattern_min_y = min(p[1] for p in pattern)
		self.pattern = [(p[0]-pattern_min_x, p[1]-pattern_min_y) for p in pattern]
		self.gathered = False
		self.finished = False
		self.destination = None
		self.local_coordinate = (0, 0)
		self.n = len(self.pattern)

	def generate_transition(self,local_vertex_mapping):
		direction = "S"
		# Do nothing when finished
		if not self.finished:
			if self.gathered:
				direction = self.generate_transition_pattern(local_vertex_mapping)
			else:
				direction = self.generate_transition_gather(local_vertex_mapping)
		self.local_coordinate = get_local_coords_from_movement(self.local_coordinate[0], self.local_coordinate[1], direction)
		return self.location.state, self.state, direction 

	def generate_transition_gather(self, local_vertex_mapping):
		# Local Search
		local_agent_dict = {}
		for coord in local_vertex_mapping.keys():
			a_num = len(local_vertex_mapping[coord].agents)
			if a_num > 0:
				local_agent_dict[coord] = a_num
		if sum(local_agent_dict.values()) == self.n:
			min_x = min(c[0] for c in local_agent_dict.keys())
			min_y = min(c[1] for c in local_agent_dict.keys())
			max_x = max(c[0] for c in local_agent_dict.keys())
			max_y = max(c[1] for c in local_agent_dict.keys())
			if max_y - min_y <= INFLUENCE_RADIUS and max_x - min_x <= INFLUENCE_RADIUS:
				self.gathered = True
				self.local_coordinate = (-min_x, -min_y)
				self.pick_destination(self.pattern)
				print(self.id, "Gathered", self.local_coordinate)
			return "S"
		dest_x = int(sum(coord[0] for coord in local_agent_dict.keys())/len(local_agent_dict))
		dest_y = int(sum(coord[1] for coord in local_agent_dict.keys())/len(local_agent_dict))
		direction = get_direction(0, 0, dest_x, dest_y) 
		return direction

	def generate_transition_pattern(self,local_vertex_mapping):
		# check all destinations
		taken_destination = []
		for p in self.pattern:
			dx = p[0] - self.local_coordinate[0]
			dy = p[1] - self.local_coordinate[1]
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
		if (self.destination[0] == self.local_coordinate[0] and self.destination[1] == self.local_coordinate[1] ):
			current_vertex = local_vertex_mapping[(0, 0)] 
			count = len(current_vertex.agents) 
			if count == 1:
				print(self.id, "done!")
				self.finished = True
				return "S"
			elif random.random() < 1/count:
				return "S"
			else:
				return random.choice(["U", "D", "L", "R"])
		#Move to target
		return get_direction(self.local_coordinate[0], self.local_coordinate[1], self.destination[0], self.destination[1])

	def pick_destination(self, pattern):
		if len(pattern) == 0:
			return
		self.destination = None
		dist_l = [abs(p[0] - self.location.x) + abs(p[1] - self.location.y) for p in pattern]
		weight_l = [1/d for d in dist_l]
		self.destination = random.choices(pattern, weights=weight_l)[0]
		print("Agent ", self.id, "chooses destination to ", self.destination)


def get_direction(x, y, dest_x, dest_y):
	if x == dest_x and y == dest_y:
		return "S"
	possible_moves = []
	if x < dest_x:
		possible_moves.append("R")
	if x > dest_x:
		possible_moves.append("L")
	if y < dest_y:
		possible_moves.append("U")
	if y > dest_y:
		possible_moves.append("D")
	return random.choice(possible_moves)

def get_local_coords_from_movement(x, y, direction):
	if direction == "S":
		return x, y
	elif direction == "L":
		return x-1, y
	elif direction == "R":
		return x+1, y
	elif direction == "D":
		return x, y-1
	elif direction == "U":
		return x, y+1
	return x, y
