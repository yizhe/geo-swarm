from AgentState import AgentState

class Agent:
	def __init__(self,id, vertex):
		self.id = id
		self.state = AgentState()
		self.location = vertex

	def generate_transition(self,local_vertex_mapping):
		return self.location.state, self.state, "S"

