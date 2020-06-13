import pygame
import time


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
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)

	def draw(self,win):
		self.move()
		self.smoke()
		for rectangle in self.smoke_trail:
			win.blit(cloud_img, (rectangle[0],rectangle[1]))
		win.blit(spaceship_img[self.dir_index], (self.x, self.y))

		self.hitbox_pos()

		#pygame.draw.rect(win, (255,0,0), self.hitbox,2)
		#commented out code that makes hitbox visible
	

	def hitbox_pos(self):
		#adjusts hitbox positioning depending on the spaceship direction
		#if moving left
		if self.dirx == -1:
			self.hitbox = (self.x + 13, self.y + 6, 60, 37)
		#if moving right
		elif self.dirx == 1:
			self.hitbox = (self.x + 23, self.y + 6 ,60, 37)
		#if moving up
		elif self.diry == -1:
			self.hitbox = (self.x + 6, self.y + 13,37, 60)
		#else, I must be moving down
		else:
			self.hitbox = (self.x + 6, self.y + 23 , 37, 60)
		

	def move(self):
		keys = pygame.key.get_pressed()

		for key in keys:
			if keys[pygame.K_LEFT] and self.dirx != 1:
				self.dirx = -1
				self.diry = 0
				self.dir_index = 0
			elif keys[pygame.K_RIGHT] and self.dirx != -1:
				self.dirx = 1
				self.diry = 0
				self.dir_index = 1
			elif keys[pygame.K_UP] and self.diry != 1:
				self.dirx = 0
				self.diry = -1
				self.dir_index = 2
			elif keys[pygame.K_DOWN] and self.diry != -1:
				self.dirx = 0
				self.diry = 1
				self.dir_index = 3

		self.x += self.vel * self.dirx
		self.y += self.vel * self.diry

	def smoke(self):
		#adds in smoke cloud positions to a list
		self.smoke_count += 1
		if self.smoke_count % 7 == 0:
			self.smoke_trail.append(pygame.Rect(self.x, self.y,30,30))

	def collision(self):
		#consider pulling this out of the class 
		#if moving left
		if self.dirx == -1 and self.hitbox[0] <= 0:
			return True
		#if moving right
		elif self.dirx == 1 and self.hitbox[0] >= 980:
			return True
		#if moving up
		elif self.diry == -1 and self.hitbox[1] <= 0:
			return True
		#else, I must be moving down
		elif self.diry == 1 and self.hitbox[1] >= 780:
			return True
		
		
		if len(self.smoke_trail) > 5:
			wall = self.smoke_trail[:len(self.smoke_trail)-5]
			spaceship_rect = pygame.Rect(self.hitbox)
			if spaceship_rect.collidelist(wall) > -1:
				return True

def redrawGameWindow(win, player):
	game_over = 0
	win.blit(bg, (0,0))
	player.draw(win)
	#determine which way the enemy spaceship is moving
	#draw the enemy spaceship
	if player.collision():
		game_over = 1
	pygame.display.update()

	return game_over

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont('arial', 50, True)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def showGameStartScreen(win, width, height):
	clock = pygame.time.Clock()
	win.blit(bg, (0,0))
	draw_text(win, "Galaxy Racers", 64, width / 2, height / 4)
	draw_text(win, "Use arrow keys to move", 22, width/ 2, height / 2)
	draw_text(win, "Press a key to begin", 18, width / 2, height * 3 / 4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return False
			if event.type == pygame.KEYUP:
				waiting = False
				return True

def computerMovement():
	#change the class values for dirx, diry, and index
	pass

def main():
	pygame.init()
	screen_width = 1000
	screen_height = 800
	win = pygame.display.set_mode((screen_width,screen_height))

	showGameStartScreen(win, screen_width, screen_height)

	player = spaceship(300,300,0, -1)

	# Variable to keep the main loop running
	running = True

	# Main loop
	while running:
		# Did the user click the window close button? If so, stop the loop.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if redrawGameWindow(win,player):
			if showGameStartScreen(win,screen_width,screen_height):
				player = spaceship(300,300,0, -1)
			else:
				pygame.quit()


			

main()