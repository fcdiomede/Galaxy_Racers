import pygame

bg = pygame.image.load('bg.jpg')
spaceship_img = pygame.image.load('spacecraft_pink.png')

class spaceship(object):
	def __init__(self, x,y, dirx, diry):
		self.x = x
		self.y = y
		self.dirx = diry
		self.diry = dirx
		self.vel = 5

	def draw(self,win):
		self.move()
		win.blit(spaceship_img, (self.x, self.y))

	def move(self):
		keys = pygame.key.get_pressed()

		for key in keys:
			if keys[pygame.K_LEFT]:
				self.dirx = -1
				self.diry = 0
			elif keys[pygame.K_RIGHT]:
				self.dirx = 1
				self.diry = 0
			elif keys[pygame.K_UP]:
				self.dirx = 0
				self.diry = -1
			elif keys[pygame.K_DOWN]:
				self.dirx = 0
				self.diry = 1

		self.x += self.vel * self.dirx
		self.y += self.vel * self.diry

	def collision(self):
		pass


def redrawGameWindow(win):
	global player
	win.blit(bg, (0,0))
	player.draw(win)
	pygame.display.update()

def main():
	global player
	pygame.init()
	screen_width = 1000
	screen_height = 800
	win = pygame.display.set_mode((screen_width,screen_height))

	clock = pygame.time.Clock()

	player = spaceship(300,300,-1, 0)

	# Variable to keep the main loop running
	running = True

	# Main loop
	while running:
		# Did the user click the window close button? If so, stop the loop.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		redrawGameWindow(win)

	pygame.quit()

main()