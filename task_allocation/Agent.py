from AgentState import AgentState
from geo_utils import *
import random
from math import pi, floor
from constants import *
from scipy.stats import levy
import copy

class Agent:
	def __init__(self,agent_id, vertex, l=L):
		self.location = vertex
		self.state = AgentState(agent_id, vertex, l)

	def find_nearby_task(self,local_vertex_mapping):
		ret = None
		min_dist = 10000000000
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			if vertex.state.is_task and vertex.state.residual_demand > 0:
				this_dist = l2_distance(self.location.x, self.location.y, self.location.x+dx, self.location.y+dy)
				if  this_dist < min_dist:
					min_dist = this_dist
					ret = vertex.state
		return ret

	# def num_neighbors(self, local_vertex_mapping):
	# 	agents_sensed = 0 
	# 	for dx, dy in local_vertex_mapping.keys():
	# 		agents_sensed += len(local_vertex_mapping[(dx,dy)].agents)
	# 	return agents_sensed

	# def random_location_in_site(self, site):
	# 	x_range = site.site_location[0]
	# 	y_range = site.site_location[1]

	# 	return (random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1]))

	def within_site(self, x, y, site):
		if site == None:
			x_range = (0, M-1)
			y_range = (0, N-1)
		# else:
		# 	x_range = site.site_location[0]
		# 	y_range = site.site_location[1]

		if x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]:
			return True
		return False


	def get_travel_direction(self, new_agent_state):
		if self.state.travel_distance == 0:
			new_agent_state.travel_distance = int(min(self.state.levy_cap, levy.rvs(loc=levy_loc))) #Twice the distance to the nest? maybe make this a variable
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)

		new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
		new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)


		# If the agent is about to walk out of bounds, try again
		bounding_site = None
		# if self.state.preference_type == "Uncommitted":
		# 	bounding_site = self.destination_site
		# elif self.state.preference_type == "Favoring" and self.state.activity_type == "Active":
		# 	bounding_site = self.favored_site
		# elif self.state.preference_type == "Favoring":
		# 	if self.exploring_site:
		# 		bounding_site = self.destination_site
		# 	else:
		# 		bounding_site = self.home_nest
		# elif self.state.preference_type == "Quorum":
		# 	if self.state.activity_type == "Nest":
		# 		bounding_site = self.home_nest


		while not self.within_site(new_location[0], new_location[1], bounding_site):
			new_agent_state.angle = random.uniform(0, 2*pi)
			new_agent_state.starting_point = (self.location.x, self.location.y)
			new_direction = get_direction_from_angle(new_agent_state.angle, new_agent_state.starting_point, (self.location.x, self.location.y))
			new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)
		new_agent_state.travel_distance = new_agent_state.travel_distance-1
		return new_direction



	def generate_transition(self,local_vertex_mapping):
		new_agent_state = copy.copy(self.state)
		# We are not headed towards a task or doing a task
		if self.state.committed_task is None and self.state.destination_task is None:
			nearby_task = self.find_nearby_task(local_vertex_mapping)
			if nearby_task is not None:
				new_agent_state.destination_task = nearby_task
				return self.location.state, new_agent_state, "S"
			else:
				new_direction = self.get_travel_direction(new_agent_state)
				return self.location.state, new_agent_state, new_direction
		# We are headed towards a task
		if self.state.destination_task is not None:
			if self.state.destination_task.residual_demand == 0:
				new_agent_state.destination_task = None
				return self.location.state, new_agent_state, "S"
			# If we have arrived
			if self.location.coords() == self.state.destination_task.task_location:
				new_agent_state.committed_task = self.state.destination_task
				new_agent_state.destination_task = None
				new_vertex_state = copy.copy(self.location.state)
				new_vertex_state.residual_demand = self.location.state.residual_demand-1
				print(new_vertex_state.residual_demand)
				return new_vertex_state, new_agent_state, "S"
			# Still headed towards task
			else:
				new_direction = get_direction_from_destination(self.state.destination_task.task_location, self.location.coords())
				new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
				return self.location.state, new_agent_state, new_direction 
		# We are committed to doing a task, so stay still
		else:
			return self.location.state, self.state, "S"



		# if self.state.core_state == "Home":
		# 	# For random walking should all explore
		# 	explore_chance = 1
		# 	if random.random() < explore_chance:
		# 		return self.location.state, AgentState("Uncommitted", "Active"), "S"
		# 	else:
		# 		return self.location.state, self.state, "S"

		# return self.location.state, self.state, "S"

