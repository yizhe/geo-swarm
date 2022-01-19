from AgentState import AgentState
import random

class Agent:
	def __init__(self,id, vertex):
		self.id = id
		self.state = AgentState()
		self.location = vertex

	def get_coords_from_movement(self,direction, x, y):
		if direction == "L":
			return x-1, y
		elif direction == "R":
			return x+1, y
		elif direction == "U":
			return x, y+1
		elif direction == "D":
			return x, y-1
		else:
			return x,y

	def transition(self,nearby_agents):
		# Depends on the application
		direction_map = {0:"S", 1:"L", 2:"R", 3:"U", 4:"D"}

		# Try to spread out
		if len(nearby_agents) == 0:
			return self.state, "S"
		total_dist = 0
		for agent in nearby_agents:
			total_dist += min(abs(self.location.x-agent.location.x), 50-abs(self.location.x-agent.location.x))
			total_dist += min(abs(self.location.y-agent.location.y), 50-abs(self.location.y-agent.location.y))

		best_moves = []
		best_distance = 100000
		print("hi")
		for direction in direction_map.values():
			new_loc = self.get_coords_from_movement(direction, self.location.x, self.location.y)

			dist = 0
			for agent in nearby_agents:
				dist += min(abs(new_loc[0]-agent.location.x), 50-abs(new_loc[0]-agent.location.x))+min(abs(new_loc[1]-agent.location.y), 50-abs(new_loc[1]-agent.location.y))
			if dist < best_distance:
				best_distance = dist
				best_moves = [direction]
			if dist == best_distance:
				best_moves.append(direction)
		return self.state, random.choice(best_moves)

		# Random direction movement
		# return self.state, direction[randint(0,4)] 


