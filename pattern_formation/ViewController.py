import pygame
import sys 

class ViewController:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 200, 0)
	ORANGE = (255, 191, 0)
	RED = (200, 0, 0)
	VERTEX_SIZE = 20
	FPS = 2

	def __init__(self, configuration):
		self.configuration = configuration
		self.WINDOW_HEIGHT = self.configuration.Y_MAX*self.VERTEX_SIZE
		self.WINDOW_WIDTH = self.configuration.X_MAX*self.VERTEX_SIZE
		pygame.init()
		self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.SCREEN.fill(self.WHITE)
		self.make_grid()
		
		self.font = pygame.font.SysFont(None, 20)

	def make_grid(self):
		
		for x in range(0, self.configuration.X_MAX):
			for y in range(0, self.configuration.Y_MAX):
				rect = pygame.Rect(x*self.VERTEX_SIZE, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE, self.VERTEX_SIZE, self.VERTEX_SIZE)
				pygame.draw.rect(self.SCREEN, self.BLACK, rect, 1)
		pygame.display.update()

	def draw_configuration(self):
		for x in range(0, self.configuration.X_MAX):
			for y in range(0, self.configuration.Y_MAX):
				rect = self.get_rect(x, y)
				num_agents = len(self.configuration.vertices[(x,y)].agents)
				if num_agents > 10:
					pygame.draw.rect(self.SCREEN, (255, 0, 0), rect, 0)
				elif num_agents > 5:
					pygame.draw.rect(self.SCREEN, (255, 255, 0), rect, 0)
				elif num_agents > 0:
					pygame.draw.rect(self.SCREEN, self.GREEN, rect, 0)
				elif (x,y) in self.configuration.pattern:
					pygame.draw.rect(self.SCREEN, self.ORANGE, rect, 0)
				else:
					pygame.draw.rect(self.SCREEN, self.WHITE, rect, 0)
				if num_agents > 0:
					num_agents_text = self.font.render(str(num_agents), True, self.BLACK)
					self.SCREEN.blit(num_agents_text, 
							(x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1))
		for agent in self.configuration.agents.values():
			if agent.destination:
				if hasattr(agent, "local_coordinate"):
					target_x = agent.destination[0] + agent.location.x - agent.local_coordinate[0]
					target_y = agent.destination[1] + agent.location.y - agent.local_coordinate[1]
					self.draw_line(agent.location.x, agent.location.y, target_x, target_y)
				else:
					self.draw_line(agent.location.x, agent.location.y, agent.destination[0], agent.destination[1])

	def get_rect(self, x, y):
		return pygame.Rect(x*self.VERTEX_SIZE+1, self.WINDOW_HEIGHT-y*self.VERTEX_SIZE-self.VERTEX_SIZE+1, self.VERTEX_SIZE-2, self.VERTEX_SIZE-2)

	def draw_line(self, x0, y0, x1, y1):
		pygame.draw.line(self.SCREEN, self.RED, 
				(int((x0+0.5) * self.VERTEX_SIZE), self.WINDOW_HEIGHT - int((y0+0.5) * self.VERTEX_SIZE)),
				(int((x1+0.5) * self.VERTEX_SIZE), self.WINDOW_HEIGHT - int((y1+0.5) * self.VERTEX_SIZE)), width=2)

	def update(self):
		self.draw_configuration()
		self.make_grid()
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.time.delay(int(1000/self.FPS))

	def quit(self):
		pygame.quit()
		sys.exit()
