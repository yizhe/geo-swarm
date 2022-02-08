directions = {"S", "L", "R", "D", "U"}
from constants import N, M, TORUS

"""
Given a vertex location (x,y), generate a map from local coordinates to other vertices

Parameters
vertex: Vertex
	the central vertex from which to generate the local map around 
influence_radius: int
	generate the map with vertices in the square {-d, +d} around the 
	central vertex, where d is the influence radius 
global_vertices: dict
	mapping from locations (x,y) to Vertex from the global configuration
"""
def generate_local_mapping(vertex, influence_radius, global_vertices):

	vertex_mapping = {}
	vx = vertex.x
	vy = vertex.y

	for dx in range(-influence_radius,influence_radius+1):
		for dy in range(-influence_radius,influence_radius+1):
			if TORUS:
				vertex_mapping[(dx, dy)] = global_vertices[(vx+dx)%M, (vy+dy)%N]
			else:
				if vx + dx < M and vx + dx >= 0 and vy+dy < N and vy+dy >= 0:
					vertex_mapping[(dx, dy)] = global_vertices[vx+dx, vy+dy]

	return vertex_mapping

"""
Given a direction of motion, computes the new coordinate 
Parameters
x: int
	the x coordinate of original location
y: int 
	the y coordinate of original location
direction: str
	{S, D, U, L, R} representing which direction to move
"""
def get_coords_from_movement(x, y, direction):
	if direction == "S":
		return x, y
	elif direction == "L":
		if x-1 >= 0:
			return x-1, y
		elif TORUS:
			return (x-1)%M, y
	elif direction == "R":
		if x+1 < M:
			return x+1, y
		elif TORUS:
			return (x+1)%M, y
	elif direction == "D":
		if y-1 >= 0:
			return x, y-1
		elif TORUS:
			return x, (y-1)%N
	elif direction == "U":
		if y+1 < N:
			return x, y+1
		elif TORUS:
			return x, (y+1)%N
	return x, y