import pygame

bg = pygame.image.load('bg.jpg')
spaceship_img = [pygame.image.load('spacecraft_left.png'),pygame.image.load('spacecraft_right.png'),pygame.image.load('spacecraft_up.png'),pygame.image.load('spacecraft_down.png')]
cloud_img = pygame.image.load('cloud.png')

class spaceship(object):
	def __init__(self, x,y, dirx, diry):
		self.x = x
		self.y = y
		self.dirx = diry
		self.diry = dirx
		self.vel = 5
		self.dir_index = 0
		self.smoke_trail = []
		self.smoke_count = 0

	def draw(self,win):
		self.move(win)
		win.blit(spaceship_img[self.dir_index], (self.x, self.y))
		for pos in self.smoke_trail:
			win.blit(cloud_img, pos)
		

	def move(self,win):
		keys = pygame.key.get_pressed()

		for key in keys:
			if keys[pygame.K_LEFT]:
				self.dirx = -1
				self.diry = 0
				self.dir_index = 0
			elif keys[pygame.K_RIGHT]:
				self.dirx = 1
				self.diry = 0
				self.dir_index = 1
			elif keys[pygame.K_UP]:
				self.dirx = 0
				self.diry = -1
				self.dir_index = 2
			elif keys[pygame.K_DOWN]:
				self.dirx = 0
				self.diry = 1
				self.dir_index = 3

		self.smoke_count += 1
		if self.smoke_count % 7 == 0:
			self.smoke_trail.append((self.x,self.y))
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

	player = spaceship(300,300,0, -1)

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