from VertexState import VertexState
class Vertex:
	def __init__(self,x,y):
		self.x = x
		self.y = y 
		self.agents = set()
		self.state = VertexState()