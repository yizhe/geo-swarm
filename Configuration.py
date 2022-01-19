import multiprocessing as mp
from Agent import Agent
from Vertex import Vertex

class Configuration:
	# Graph is a N by M grid
	def __init__(self, agent_locations, N, M, torus=False):
		# Create all vertices
		self.vertices = {}
		for x in range(M):
			for y in range(N):
				self.vertices[(x, y)] = Vertex(x,y)
		self.torus = torus
		self.N = N
		self.M = M
		self.influence_radius = 7 # make this a class variable later; radius 0 means only self is influenced
		self.agents = {} # map from id to agent itself
		
		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, location)
			self.agents[agent_id] = agent
			location.agents.add(agent)

	# Will need to be made more complex to account for conflicting vertex states
	def merge(self, local_transitions):
		global_transition = {}
		for local_transition in local_transitions:
			for key in local_transition.keys():
				global_transition[key] = local_transition[key]
		return global_transition

	def generate_transition(self):
		# pool = mp.Pool(mp.cpu_count())
		# transitories = [pool.apply(self.vertex_transition, args = (row, col)) for row in range(N) for col in range (M)]
		# pool.close()

		vertex_transitions = []
		for x in range(self.M):
			for y in range(self.N):
				vertex_transitions.append(self.vertex_transition(x,y))

		#Merge all the local transitions
		return self.merge(vertex_transitions)

	"""
	thought: what if we are doing something like foraging and both agents are trying to take an object.
	each agent may have a different proposed state for the vertex, in which case ties are broken randomly
	agents who do not get their proposed vertex state do not get to change their own state either 
	TODO: incorporate changes to vertex state.
	TODO: incorpoate message sending
	"""
	def vertex_transition(self,x,y):
		vertex = self.vertices[(x,y)]

		neighboring_agents = []
		for nx in range(vertex.x-self.influence_radius,vertex.x+self.influence_radius+1):
			for ny in range(vertex.y-self.influence_radius, vertex.y+self.influence_radius+1):
				#if n_row == row and n_col == col: continue

				local_agents = []

				if self.torus:
					local_agents = self.vertices[(nx%self.M, ny%self.N)].agents
					
				else:
					if nx >= 0 and nx < self.M and ny >= 0 and ny < self.N:
						local_agents = self.vertices[(nx,ny)].agents
				for agent in local_agents:
					neighboring_agents.append(agent)

		transitions = {}
		for agent in vertex.agents:
			transitions[agent.id] = agent.transition(neighboring_agents)

		return transitions

	def execute_transition(self,transition):
		for agent_id in transition.keys():
			agent = self.agents[agent_id]
			curr_vertex = agent.location

			agent.state = transition[agent_id][0]
			movement_dir = transition[agent_id][1]

			# Erase agent from current location
			curr_vertex.agents.remove(agent)

			# S means stay at the same location
			if movement_dir == "S":
				pass 
			elif movement_dir == "L":
				if curr_vertex.x-1 >= 0:
					agent.location = self.vertices[(curr_vertex.x-1, curr_vertex.y)]
				elif self.torus:
					agent.location = self.vertices[((curr_vertex.x-1)%self.M, curr_vertex.y)]
			elif movement_dir == "R":
				if curr_vertex.x+1 < self.M:
					agent.location = self.vertices[(curr_vertex.x+1, curr_vertex.y)]
				elif self.torus:
					agent.location = self.vertices[((curr_vertex.x+1)%self.M, curr_vertex.y)]
			elif movement_dir == "D":
				if curr_vertex.y-1 >= 0:
					agent.location = self.vertices[(curr_vertex.x, curr_vertex.y-1)]
				elif self.torus:
					agent.location = self.vertices[(curr_vertex.x, (curr_vertex.y-1)%self.N)]
			elif movement_dir == "U":
				if curr_vertex.y+1 < self.N:
					agent.location = self.vertices[(curr_vertex.x, curr_vertex.y+1)]
				elif self.torus:
					agent.location = self.vertices[(curr_vertex.x, (curr_vertex.y+1)%self.N)]

			# Add agent to updated location
			agent.location.agents.add(agent)

	def transition(self):
		transitory_state = self.generate_transition()
		self.execute_transition(transitory_state)



