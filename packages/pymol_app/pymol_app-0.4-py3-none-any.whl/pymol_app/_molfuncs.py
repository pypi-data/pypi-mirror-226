#!/usr/bin/env python

import pygame
import random
import math

def interpolate_color(color1, color2, t):
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def pulse_screen(screen, clock):

	start_time = pygame.time.get_ticks()

	# Colors
	color1 = (50, 50, 50)
	color2 = (200, 200, 200)

	# Number of frames for the transition
	freq = .5
	dur = random.uniform(5, 10)

	while 1:
		current_time = pygame.time.get_ticks()

		elapsed_time = (current_time - start_time) / 1000.0  # Convert to seconds

		if elapsed_time >= dur:
			break

		# Calculate the oscillation parameter between 0 and 1
		oscillation_parameter = 0.5 + 0.5 * math.sin(2 * math.pi * freq * elapsed_time)

		# Calculate the interpolated color based on the oscillation parameter
		current_color = interpolate_color(color1, color2, oscillation_parameter)

		# Fill the screen with the current color
		screen.fill(current_color)

		# Update the display
		pygame.display.flip()

		# Cap the frame rate
		clock.tick(60)