import pygame
import sys 

class ViewController:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 200, 0)
	VERTEX_SIZE = 20
	FPS = 2

	def __init__(self, configuration):
		self.configuration = configuration
		self.WINDOW_HEIGHT = self.configuration.N*self.VERTEX_SIZE
		self.WINDOW_WIDTH = self.configuration.M*self.VERTEX_SIZE
		pygame.init()
		self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.make_grid()
		

	def make_grid(self):
		self.SCREEN.fill(self.WHITE)
		for row in range(0, self.configuration.N):
			for col in range(0, self.configuration.M):
				rect = pygame.Rect(col*self.VERTEX_SIZE, row*self.VERTEX_SIZE, self.VERTEX_SIZE, self.VERTEX_SIZE)
				pygame.draw.rect(self.SCREEN, self.BLACK, rect, 1)
		pygame.display.update()

	def draw_configuration(self):
		for row in range(0, self.configuration.N):
			for col in range(0, self.configuration.M):
				rect = pygame.Rect(col*self.VERTEX_SIZE+1, row*self.VERTEX_SIZE+1, self.VERTEX_SIZE-2, self.VERTEX_SIZE-2)
				if len(self.configuration.vertices[(row, col)].agents) > 10:
					pygame.draw.rect(self.SCREEN, (255, 0, 0), rect, 0)
				elif len(self.configuration.vertices[(row, col)].agents) > 5:
					pygame.draw.rect(self.SCREEN, (255, 255, 0), rect, 0)
				elif len(self.configuration.vertices[(row, col)].agents) > 0:
					pygame.draw.rect(self.SCREEN, self.GREEN, rect, 0)
				else:
					pygame.draw.rect(self.SCREEN, self.WHITE, rect, 0)

	def update(self):
		self.draw_configuration()
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.time.delay(int(1000/self.FPS))

	def quit(self):
		pygame.quit()
		sys.exit()
