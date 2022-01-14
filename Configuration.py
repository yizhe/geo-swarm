import multiprocessing as mp
from Agent import Agent
from Vertex import Vertex

class Configuration:
	# Graph is a N by M grid
	def __init__(self, agent_locations, N, M, torus=False):
		# Create all vertices
		self.vertices = {}
		for row in range(N):
			for col in range(M):
				self.vertices[(row, col)] = Vertex(row,col)
		self.torus = torus
		self.N = N
		self.M = M
		self.influence_radius = 2 # make this a class variable later; radius 0 means only self is influenced
		self.agents = {} # map from id to agent itself
		for agent_id in range(len(agent_locations)):
			location = self.vertices[agent_locations[agent_id]]
			agent = Agent(agent_id, self.vertices[agent_locations[agent_id]])
			self.agents[agent_id] = agent
			location.agents.add(agent)

	def generate_transition(self):
		# pool = mp.Pool(mp.cpu_count())
		# transitories = [pool.apply(self.vertex_transition, args = (row, col)) for row in range(N) for col in range (M)]
		# pool.close()
		transitories = [self.vertex_transition(row, col) for row in range(self.N) for col in range (self.M)]

		#Merge all the local transitions
		global_transition = {}
		for local_transition in transitories:
			for key in local_transition.keys():
				global_transition[key] = local_transition[key]
		return global_transition

	"""
	thought: what if we are doing something like foraging and both agents are trying to take an object.
	each agent may have a different proposed state for the vertex, in which case ties are broken randomly
	agents who do not get their proposed vertex state do not get to change their own state either 
	TODO: incorporate changes to vertex state.
	TODO: incorpoate message sending
	"""
	def vertex_transition(self,row, col):
		vertex = self.vertices[(row,col)]

		neighboring_agents = []
		for row in range(vertex.row-self.influence_radius,vertex.row+self.influence_radius+1):
			for col in range(vertex.col-self.influence_radius, vertex.col-self.influence_radius+1):
				local_agents = []

				if self.torus:
					local_agents = self.vertices[(row%self.N, col%self.M)].agents
					
				else:
					if row >= 0 and row < self.N and col >= 0 and col < self.M:
						local_agents = self.vertices[(row,col)].agents
				print(len(local_agents))
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
			agent.location.agents.remove(agent)

			# S means stay at the same location
			if movement_dir == "S":
				pass 
			elif movement_dir == "L":
				if curr_vertex.col-1 >= 0:
					agent.location = self.vertices[(curr_vertex.row, curr_vertex.col-1)]
				elif self.torus:
					agent.location = self.vertices[(curr_vertex.row, (curr_vertex.col-1)%self.M)]
			elif movement_dir == "R":
				if curr_vertex.col+1 < self.M:
					agent.location = self.vertices[(curr_vertex.row, curr_vertex.col+1)]
				elif self.torus:
					agent.location = self.vertices[(curr_vertex.row, (curr_vertex.col+1)%self.M)]
			elif movement_dir == "U":
				if curr_vertex.row-1 >= 0:
					agent.location = self.vertices[(curr_vertex.row-1, curr_vertex.col)]
				elif self.torus:
					agent.location = self.vertices[((curr_vertex.row-1)%self.N, curr_vertex.col)]
			elif movement_dir == "D":
				if curr_vertex.row+1 < self.N:
					agent.location = self.vertices[(curr_vertex.row+1, curr_vertex.col)]
				elif self.torus:
					agent.location = self.vertices[((curr_vertex.row+1)%self.N, curr_vertex.col)]

			# Add agent to updated location
			agent.location.agents.add(agent)

	def transition(self):
		transitory_state = self.generate_transition()
		self.execute_transition(transitory_state)



