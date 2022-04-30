from AgentState import AgentState
from geo_utils import *
import random
from math import pi, floor
from constants import L, levy_loc, levy_cap, QUORUM_THRESHOLD, MESSAGE_RATE, Q_MIN, Q_MAX, INF
from scipy.stats import levy

class Agent:
	def __init__(self,agent_id, vertex, home_nest, l=L):
		self.reset(agent_id, vertex, home_nest, l)

	def reset(self, agent_id, vertex, home_nest, l):
		self.id = agent_id
		self.state = AgentState()
		self.location = vertex
		self.home_nest = home_nest

		# Constant config params
		self.MESSAGE_RATE = MESSAGE_RATE
		#Random walk parameters
		self.angle = 0 # an angle from [0,2pi)
		self.starting_point = (vertex.x, vertex.y) # where the agent originated
		self.travel_distance = 0 # how many more steps the agent has to venture

		#Destination travel parameters
		self.destination = None
		self.destination_site = None

		#Whether uncommitted agent is exploring the site it is in
		self.exploring_site = False
		self.exploration_cooldown = 0 #Time before accepting a new site if just rejected one 

		#Abandonment parameter
		self.time_since_neighbor = 0

		self.favored_site = None
		self.quorum_site = None

		self.terminated = False

		self.L = l
		self.levy_cap = 1/l

	def find_nearby_site(self,local_vertex_mapping):
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			if vertex.state.site_name is not None and vertex.state.site_name != "Home" and vertex.state.site_entrance == None:
				return vertex.state, (self.location.x+dx, self.location.y+dy)
			# elif vertex.state.site_name is not None and vertex.state.site_name != "Home":
			# 	entrance_local_coords = (vertex.state.site_entrance[0]-self.location.x, vertex.state.site_entrance[1]-self.location.y)
			# 	if entrance_local_coords in local_vertex_mapping:
			# 		return local_vertex_mapping[entrance_local_coords], vertex.state.site_entrance
		return None, (None, None)

	def find_better_nest(self, local_vertex_mapping):
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				if agent != self and agent.state.preference_type == "Favoring" and agent.favored_site.site_value > self.favored_site.site_value and random.random() < self.MESSAGE_RATE:
					return agent.favored_site
		return None

	def num_neighbors(self, local_vertex_mapping):
		agents_sensed = 0 
		for dx, dy in local_vertex_mapping.keys():
			agents_sensed += len(local_vertex_mapping[(dx,dy)].agents)
		return agents_sensed
		
	def quorum_threshold(self, site_value):
		if site_value is not None:
			return floor((Q_MIN-Q_MAX)*site_value + Q_MAX)
		return INF

	def quorum_sensed(self, local_vertex_mapping):
		agents_sensed_in_site = 0
		for dx, dy in local_vertex_mapping.keys():
			vertex = local_vertex_mapping[(dx,dy)]
			for agent in vertex.agents:
				if agent.quorum_site != None:
					return agent.quorum_site
			if self.state.preference_type == "Favoring" and self.state.activity_type == "Active" and vertex.state == self.favored_site:
				agents_sensed_in_site += len(vertex.agents)
			if self.state.preference_type == "Uncommitted" and self.state.activity_type == "Active":
				if self.location.state.site_name != "Home" and self.location.state.site_name is not None:
					agents_sensed_in_site += len(vertex.agents) #ASSSUMES THAT YOU WOULD ONLY SENSE ONE SITE AT A TIME
		if self.state.preference_type == "Favoring" and agents_sensed_in_site > self.quorum_threshold(self.favored_site.site_value):
			return self.favored_site
		if self.state.preference_type == "Uncommitted" and agents_sensed_in_site > self.quorum_threshold(self.location.state.site_value):
			return self.location.state
		return None

	def random_location_in_site(self, site):
		# if site.site_entrance != None:
		# 	return site.site_entrance

		x_range = site.site_location[0]
		y_range = site.site_location[1]

		return (random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1]))

	def within_site(self, x, y, site):
		if site == None:
			# We are trying to enter a site with only one entraance while exploring arena
			# if self.location.state.site_entrance != None:
			# 	return False
			x_range = (0, M-1)
			y_range = (0, N-1)
		else:
			x_range = site.site_location[0]
			y_range = site.site_location[1]

		if x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]:
			return True
		return False


	def check_quorum_sensed(self, local_vertex_mapping):
		quorum_site = self.quorum_sensed(local_vertex_mapping)
		if quorum_site is not None:
			self.quorum_site = quorum_site
			if random.random() < 5/10:
				self.destination = self.random_location_in_site(self.home_nest)
				self.destination_site = self.home_nest
				return True, AgentState("Quorum", "Nest")
			else:
				self.travel_distance = int(1/self.L) #Perhaps change this to higher
				self.angle = random.uniform(0,2*pi)
				self.starting_point = (self.location.x, self.location.y)
				self.destination = None
				self.destination_site = None
				return True, AgentState("Quorum", "Active")
		return False, None

	def get_travel_direction(self):
		if self.travel_distance == 0:
			self.travel_distance = max(self.levy_cap, levy.rvs(loc=levy_loc)) #Twice the distance to the nest? maybe make this a variable
			self.angle = random.uniform(0, 2*pi)
			self.starting_point = (self.location.x, self.location.y)

		new_direction = get_direction_from_angle(self.angle, self.starting_point, (self.location.x, self.location.y))
		new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)

		# If the agent is about to walk out of bounds, try again
		bounding_site = None
		if self.state.preference_type == "Uncommitted":
			bounding_site = self.destination_site
		elif self.state.preference_type == "Favoring" and self.state.activity_type == "Active":
			bounding_site = self.favored_site
		elif self.state.preference_type == "Favoring":
			if self.exploring_site:
				bounding_site = self.destination_site
			else:
				bounding_site = self.home_nest
		elif self.state.preference_type == "Quorum":
			if self.state.activity_type == "Nest":
				bounding_site = self.home_nest


		while not self.within_site(new_location[0], new_location[1], bounding_site):
			self.angle = random.uniform(0, 2*pi)
			self.starting_point = (self.location.x, self.location.y)
			new_direction = get_direction_from_angle(self.angle, self.starting_point, (self.location.x, self.location.y))
			new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction, True)

		self.travel_distance -= 1
		return new_direction



	def generate_transition(self,local_vertex_mapping):
		if self.state.preference_type == "Uncommitted":
			# Uncommitted Nest Transitions
			if self.state.activity_type == "Nest":
				# Sense quorum
				quorum_sensed, quorum_state = self.check_quorum_sensed(local_vertex_mapping)
				if quorum_sensed:
					return self.location.state, quorum_state, "S"

				# If agent is still travelling to the nest
				if self.destination is not None:
					new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
					new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
					
					if self.within_site(new_location[0], new_location[1], self.home_nest):
						self.destination = None
						
					return self.location.state, self.state, new_direction 

				# Otherwise, agent is already at the home nest 
				active_chance = self.L/9
				if random.random() < active_chance:
					return self.location.state, AgentState("Uncommitted", "Active"), "S"
				else:
					return self.location.state, self.state, "S"
			# Uncommitted Active Transitions
			else:
				# Sense quorum
				quorum_sensed, quorum_state = self.check_quorum_sensed(local_vertex_mapping)
				if quorum_sensed:
					return self.location.state, quorum_state, "S"

				if self.destination is None and self.exploration_cooldown == 0:
					# If the agent encounters a site and isn't already exploring
					nearby_site, site_location = self.find_nearby_site(local_vertex_mapping) 
					if nearby_site is not None:
						self.destination = site_location
						self.destination_site = nearby_site
				elif self.exploration_cooldown > 0:
					self.exploration_cooldown -= 1

				# If the agent is on the way to a site
				if self.destination_site is not None:
					# If we have arrived
					if self.location.state.site_name == self.destination_site.site_name and not self.exploring_site:
						self.exploring_site = True
						self.travel_distance = 10
						self.angle = random.uniform(0, 2*pi)
						self.starting_point = (self.location.x, self.location.y)

					# Still heading towards site
					elif not self.exploring_site:
						new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
						new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
						return self.location.state, self.state, new_direction


				# Calculate if the agent should become a nest agent
				nest_chance = self.L 
				if random.random() < nest_chance and not self.exploring_site:
					self.destination = self.random_location_in_site(self.home_nest)
					return self.location.state, AgentState("Uncommitted", "Nest"), "S"
				# Calculate direction of motion for random walk
				# We have finished exploring the site 
				if self.travel_distance == 0 and self.exploring_site:
					self.destination = None
					self.exploring_site = False
					self.favored_site = self.destination_site
					self.destination_site = None

					# Choose to favor the site
					if random.random() < self.location.state.site_value:
						if random.random() < 9/10:
							self.destination = self.random_location_in_site(self.home_nest)
							self.destination_site = self.home_nest
							return self.location.state, AgentState("Favoring", "Nest"), "S"
						else:
							return self.location.state, AgentState("Favoring", "Active"), "S"
					# Reject the site
					else:
						self.exploration_cooldown = 10
						self.favored_site = None

				new_direction = self.get_travel_direction()
				return self.location.state, self.state, new_direction
		elif self.state.preference_type == "Favoring":

			# Favoring active agent logic
			if self.state.activity_type == "Active":
				# Sense quorum
				quorum_sensed, quorum_state = self.check_quorum_sensed(local_vertex_mapping)
				if quorum_sensed:
					return self.location.state, quorum_state, "S"

				if self.destination is not None:
					new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
					new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
					if self.within_site(new_location[0], new_location[1], self.favored_site):
						self.destination = None
					return self.location.state, self.state, new_direction 


				nest_chance = self.L 
				if random.random() < nest_chance:
					self.destination = self.random_location_in_site(self.home_nest)
					self.destination_site = self.home_nest
					return self.location.state, AgentState("Favoring", "Nest"), "S"
				else:	
					new_direction = self.get_travel_direction()
					return self.location.state, self.state, new_direction
			# Favoring nest agent logic 
			else:
				# Abandonment logic
				if self.num_neighbors(local_vertex_mapping) > 1:
					self.time_since_neighbor = 0
				else:
					self.time_since_neighbor += 1

				if self.time_since_neighbor >= 5/self.L:
					self.angle = 0 
					self.starting_point = (self.location.x, self.location.y) 
					self.travel_distance = 0 
					self.destination = None
					self.destination_site = None
					self.exploring_site = False
					self.exploration_cooldown = 0 
					self.favored_site = None
					self.time_since_neighbor = 0

					return self.location.state, AgentState("Uncommitted", "Active"), "S"

				# Sense quorum
				quorum_sensed, quorum_state = self.check_quorum_sensed(local_vertex_mapping)
				if quorum_sensed:
					return self.location.state, quorum_state, "S"

				if self.destination is None:
					# Look at neighboring active agents and see if any of them favor a better nest; if so,
					# go check it out
					better_nest = self.find_better_nest(local_vertex_mapping)
					if better_nest is not None:
						self.destination = self.random_location_in_site(better_nest)
						self.destination_site = better_nest
				if self.destination is not None:
					if self.location.state.site_name == self.destination_site.site_name and self.destination_site != self.home_nest and not self.exploring_site:
						self.exploring_site = True
						self.travel_distance = 10
						self.angle = random.uniform(0,2*pi)
						self.starting_point = (self.location.x, self.location.y)
					# We have arrived home 
					elif self.destination_site == self.home_nest and self.location.state.site_name == self.destination_site.site_name:
						self.destination = None
						self.destination_site = None 
					elif not self.exploring_site:
						new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
						new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
						return self.location.state, self.state, new_direction 

				active_chance = self.L/9
				if random.random() < active_chance and not self.exploring_site:
					self.destination = self.random_location_in_site(self.favored_site)
					return self.location.state, AgentState("Favoring", "Active"), "S"

				if self.travel_distance == 0 and self.exploring_site:
					self.destination = None
					self.exploring_site = False

					# Choose to favor the site
					if self.location.state.site_value > self.favored_site.site_value:
						self.favored_site = self.destination_site
						self.destination_site = None
						if random.random() < 9/10:
							self.destination = self.random_location_in_site(self.home_nest)
							self.destination_site = self.home_nest
							return self.location.state, self.state, "S"
						else:
							return self.location.state, AgentState("Favoring", "Active"), "S"
					# Reject the site
					else:
						self.destination_site = None
						self.destination = self.random_location_in_site(self.home_nest)
						self.destination_site = self.home_nest
						return self.location.state, self.state, "S"

				

				new_direction = self.get_travel_direction()
				return self.location.state, self.state, new_direction

		elif self.state.preference_type == "Quorum":
			if self.terminated:
				return self.location.state, self.state, "S"

			if self.state.activity_type == "Nest":
				if self.destination_site == self.home_nest:
					if self.location.state == self.home_nest:
						self.destination = None
						self.destination_site = None
						self.travel_distance = int(1/self.L)
						self.angle = random.uniform(0,2*pi)
						self.starting_point = (self.location.x, self.location.y)
					else:
						new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
						new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
						return self.location.state, self.state, new_direction 
				if self.destination_site == self.quorum_site:
					# We have returned to the new site for good
					if self.location.x == self.destination[0] and self.location.y == self.destination[1]:
						self.destination = None
						self.destination_site = None
						self.terminated = True
						return self.location.state, self.state, "S"
					# Still heading towards the new site
					else: 
						new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
						new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
						return self.location.state, self.state, new_direction 

				#Finished broadcasting quorum, return to the quorum site
				if self.travel_distance == 0:
					self.destination = self.random_location_in_site(self.quorum_site)
					self.destination_site = self.quorum_site
					return self.location.state, self.state, "S"


				new_direction = self.get_travel_direction()
				return self.location.state, self.state, new_direction
			elif self.state.activity_type == "Active":
				# Agent is headed to the new site
				if self.destination_site == self.quorum_site:
					if self.location.x == self.destination[0] and self.location.y == self.destination[1]:
						self.destination = None
						self.destination_site = None
						self.terminated = True
						return self.location.state, self.state, "S"
					# Still heading towards the new site
					else: 
						new_direction = get_direction_from_destination(self.destination, (self.location.x, self.location.y))
						new_location = get_coords_from_movement(self.location.x, self.location.y, new_direction)
						return self.location.state, self.state, new_direction 

				# Agent is still broadcasting to others
				if self.travel_distance == 0:
					self.destination = self.random_location_in_site(self.quorum_site)
					self.destination_site = self.quorum_site
					return self.location.state, self.state, "S"

				new_direction = self.get_travel_direction()
				return self.location.state, self.state, new_direction


				



		return self.location.state, self.state, "S"









		# nearby_agents = []
		# for dx, dy in local_vertex_mapping.keys():
		# 	vertex = local_vertex_mapping[(dx,dy)]
		# 	for agent in vertex.agents:
		# 		if self != agent:
		# 			nearby_agents.append(agent)


