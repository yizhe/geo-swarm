from VertexState import VertexState
class Vertex:
	def __init__(self,row, col):
		self.row = row
		self.col = col 
		self.agents = set()
		self.state = VertexState()