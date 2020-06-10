import pygame

bg = pygame.image.load('bg.jpg')

def redrawGameWindow(win):
	win.blit(bg, (0,0))
	pygame.display.update()

def main():
	pygame.init()
	screen_width = 1000
	screen_height = 800
	win = pygame.display.set_mode((screen_width,screen_height))

	clock = pygame.time.Clock()

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