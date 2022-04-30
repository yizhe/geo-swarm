import random 
class AgentState:

	# Uncommitted, Favoring, or Quorum
	preference_types = ["Uncommitted", "Favoring", "Quorum"] 
	# Active or Nest type agents
	activity_types = ["Active", "Nest"]

	def __init__(self, preference_type=None, activity_type=None):
		if preference_type is not None:
			self.preference_type = preference_type
		else:
			self.preference_type = "Uncommitted"
		if activity_type is not None:
			self.activity_type = activity_type
		elif random.randint(1,10) <= 9:
			self.activity_type = "Nest"
		else:
			self.activity_type = "Active"




	
