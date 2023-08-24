#!/usr/bin/env python

import pygame
import csv
import argparse
from pymol_app._molfuncs import *

def app():

	parser = argparse.ArgumentParser()
	parser.add_argument("file", default='eliminatie_1.csv', nargs="?", help="The path to the dragged file")
	args = parser.parse_args()

	with open(args.file, 'r') as file:
		reader = csv.reader(file)
		kandidaten = dict(reader)

	pygame.init()

	clock = pygame.time.Clock()

	# it will display on screen
	screen = pygame.display.set_mode([600, 500], pygame.FULLSCREEN)

	# basic font for user typed
	base_font = pygame.font.Font(None, 64)
	user_text = ''

	state = 'input'

	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
			if event.type == pygame.KEYDOWN:
				
				if state == 'reveal':
					state = 'input'
					user_text = ''

				if event.key == pygame.K_ESCAPE:
					pygame.quit()

				if event.key == pygame.K_BACKSPACE:
					user_text = user_text[:-1]
					
				elif event.key == pygame.K_RETURN:
					
					if user_text in list(kandidaten.keys()):
						state = 'suspense'
					else:
						user_text = ''

				else:
					user_text += event.unicode

		if state == 'input':
			
			text_surface = base_font.render(user_text, True, "white")
			# it will set background color of screen
			bg_col = 'black'
			screen.fill(bg_col)
			# render at position stated in arguments
			screen.blit(text_surface, (screen.get_width()/2, screen.get_height()/2))

		if state == 'suspense':
			pulse_screen(screen, clock)
			state = 'reveal'

		if state == 'reveal':
			bg_col = kandidaten[user_text]
			screen.fill(bg_col)

		
		# display.flip() will update only a portion of the
		# screen to updated, not full area
		pygame.display.flip()
		
		# clock.tick(60) means that for every second at most
		# 60 frames should be passed.
		clock.tick(60)