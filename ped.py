import pygame
import sys
import random

pygame.init( )

#Ask if the user would like to make a brand new image or modify an existing image

print( "What would you like to do? new/open:" )

choice = raw_input( )

if choice == "new":
	print( "Enter width:" )
	swi = int( raw_input( ) )
	print( "Enter height:" )
	she = int( raw_input( ) )
	ssize = ( swi, she )
elif choice == "open":
	print( "Enter image path:" )
	bgp = raw_input( )
	bg = pygame.image.load( bgp )
	ssize = bg.get_size( )
	
screen = pygame.display.set_mode( ssize )

#Fill the screen with white if the image was created new or just add the image to the background if the image was opened, this ensures a non-black screen

if choice == "open":
	screen.blit( bg, bg.get_rect( ) )
elif choice == "new":
	screen.fill( ( 255, 255, 255 ) )

font = pygame.font.Font( None, 15 )

#Array of different modes for easy identifications, can add new modes by adding new list entries

mode = [ "Draw", "Erase", "AirSpray", "DrawCircle", "DrawSquare" ]

#Selected mode

cmode = 0

#Brush size

size = 5

#Rainbow mode, stored as a boolean so less memory is consumed

rb = False

#Colour variable ( R G B )

col = ( 0, 0, 0 )

#Position history for drawing lines from last mouse position to current

pos = [ ( 0, 0, 0 ), ( 0, 0, 0 ) ]

#Draw current status

def drawStat( ):
	
	#Draw background
	pygame.draw.rect( screen, ( 255, 255, 255 ), pygame.Rect( ( 0, 0 ), ( 115, 60 ) ), 0 )
	pygame.draw.rect( screen, ( 0, 0, 0 ), pygame.Rect( ( 0, 0 ), ( 115, 13 ) ), 2 )
	pygame.draw.rect( screen, ( 0, 0, 0 ), pygame.Rect( ( 0, 0 ), ( 115, 60 ) ), 2 )
	
	#Draw texts
	sbt = font.render( "Status Box", 1, ( 0, 0, 0 ) )
	screen.blit( sbt, ( 27, 2 ) )
	
	#Store the status texts in  a list so there's no need to create seperate variables that are harder to reffer to
	statustexts = [
	font.render( "Mode: " + mode[ cmode ], 1, ( 0, 0, 0 ) ),
	font.render( "Size: " + str( size ), 1, ( 0, 0, 0 ) ),
	font.render( "Colour: " + str( col ), 1, col )
	]
	
	for i in range( len( statustexts ) ):
		#Offset Y position based on which text is being drawn
		screen.blit( statustexts[ i ], ( 5, 15 + ( 15 * i ) ) )
	
def printIns( ):
				print( "\n\nLeft/Right arrow: Mode cycle\nUp/Down arrow: Size increase/decrease\nC: Colour selection\nS: Save\nI: Bring up this menu\n\n")

printIns( )

#Main loop

while 1:
	#Generates random values if rainbow mode is active
	if rb == True:
		col = ( random.randint( 0, 255 ), random.randint( 0, 255 ), random.randint( 0, 255 ) )
	#Setup event listeners
	for event in pygame.event.get( ):
		
		if event.type == pygame.QUIT:
			sys.exit( )
			
		if event.type == pygame.KEYDOWN:
			
			#Increase / Decrease selected mode depending on left / right arrow key
			if event.key == pygame.K_RIGHT:
				#Make sure a mode that doesn't exist doesn't get selected
				if cmode < len( mode ) - 1:
					cmode += 1
			elif event.key == pygame.K_LEFT:
				#Make sure a mode that doesn't exist doesn't get selected
				if cmode > 0:
					cmode -= 1
					
			#Increase / Decrease size of brush depending on up / down arrow key
			if event.key == pygame.K_UP:
				size += 1
			elif event.key == pygame.K_DOWN:
				#Make sure the size doesn't reach 0
				if size > 1:
					size -= 1
					
			#Bring up colour choice in terminal
			if event.key == pygame.K_c:
				print( "(M)anual values or (R)ainbow?:" )
				cch = raw_input( )
				if cch == "M":
					rb = False
					print( "Red:" )
					r = int( raw_input( ) )
					print( "Green:" )
					g = int( raw_input( ) )
					print( "Blue:" )
					b = int( raw_input( ) )
					#Assemble the R G and B variables into a single group for use
					col = ( r, g, b )
				elif cch == "R":
					rb = True
					
			#Save when pressing S
			if event.key == pygame.K_s:
				print( "Where?:" )
				pygame.image.save( screen, raw_input( ) )
				#Make sure the user knows the image is saved
				print( "Saved!" )
			if event.key == pygame.K_i:
				printIns( )
				
		if event.type == pygame.MOUSEMOTION:
			#Remove last mouse history index and update with new mouse position
			del pos[ 1 ]
			pos.insert( 0, event.pos )
			if event.buttons[ 0 ] == 1:
				
				#When clicking draw a circle on the first and last draw points and connect them with a line to prevent jittering brush
				if mode[ cmode ] == "Draw":
					pygame.draw.circle( screen, col, pos[ 0 ], size/2, 0 )
					pygame.draw.line( screen, col, pos[ 0 ], pos[ 1 ], size )
					pygame.draw.circle( screen, col, pos[ 1 ], size/2, 0 )
					
				if mode[ cmode ] == "Erase":
					pygame.draw.circle( screen, ( 255, 255, 255 ), pos[ 0 ], size/2, 0 )
					pygame.draw.line( screen, ( 255, 255, 255 ), pos[ 0 ], pos[ 1 ], size )
					pygame.draw.circle( screen, ( 255, 255, 255 ), pos[ 1 ], size/2, 0 )
					
				if mode[ cmode ] == "AirSpray":
					for i in range( size/2 ):
						#Draw multiple circles equal to half of the current brush size, all circles will be drawn off of the current mouse position with a random offset of -size * 5 to size * 5 
						pygame.draw.circle( screen, col, ( pos[ 0 ][ 0 ] + random.randint( -size*5, size*5 ), pos[ 0 ][ 1 ] + random.randint( -size*5, size*5 ) ), size, 0 )

		if event.type == pygame.MOUSEBUTTONDOWN:
			if mode[ cmode ] == "DrawCircle":
				pygame.draw.circle( screen, col, event.pos, size, 3 )
			
			if mode[ cmode ] == "DrawSquare":
				#Draw the square from the cursor with the top left corner being left and to the top by size/2 and the width and height being full size, this ensures that the square is drawn around the centrepoint of the cursor.
				pygame.draw.rect( screen, col, pygame.Rect( ( event.pos[ 0 ] - size/2, event.pos[ 1 ] - size/2 ), ( size, size ) ), 3 )
	
	#Draw once per loop in order to prevent things being drawn on top of
	drawStat( )
	pygame.display.update( )

