import random 
from constants import L

class AgentState:
	# Home, Exploring, Recruiting, Committed
	core_states = ["Home", "Exploring", "Recruiting", "Committed"]

	def __init__(self, agent_id, vertex, l=L):
		self.reset(agent_id, vertex, l)

	def reset(self, agent_id, vertex, l):
		# Initial Parameters
		self.core_state = "Home"
		self.id = agent_id
		self.L = l

		#Random Walk Parameters
		self.angle = 0
		self.starting_point = (vertex.x, vertex.y)
		self.travel_distance = 0
		self.levy_cap = 1/l

		#Destination Travel Parameters
		self.destination_task = None

		#Recruitment
		self.recruitment_task = None

		#Commitment
		self.committed_task = None
		
		





	
