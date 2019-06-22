#!/usr/bin/python3
import os, time
from PIL import Image
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *

os.system('import -window root /tmp/augscreen.png')
imgPIL = Image.open('/tmp/augscreen.png')
w,h = imgPIL.size
pygame.init()

#screen = pygame.display.set_mode((w,h),0,32)
screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)

img = pygame.image.load('/tmp/augscreen.png')
newSurf = pygame.Surface((w,h))
newSurf.blit(img, (0,0))

mainLoop = True
click1 = False
click2 = False
draw = False
activebutton = False
fullscreen_bt = False
fullscreen_coords = False

click1_pose = [-1,-1]
bt_save = {'x':range(-1,-1),'y':range(-1,-1)}
bt_buffer = {'x':range(-1,-1),'y':range(-1,-1)}

while mainLoop:
	for event in pygame.event.get():
		if event.type == QUIT:
				mainLoop = False
	screen.fill((255,255,255))
	screen.blit(newSurf, (0,0))
	
	if pygame.mouse.get_pressed()[0] == 1 and click1 == False and draw == True and pygame.mouse.get_pos()[0] in bt_save['x'] and pygame.mouse.get_pos()[1] in bt_save['y']:
		activebutton = True
		cropped_img = imgPIL.crop(click1_pose+mouse_pose)
		if 'Изображения' in os.listdir(os.getcwd()): cropped_img.save(os.getcwd()+'/Изображения/augscreen.png')
		else: cropped_img.save(os.getcwd()+'/Pictures/augscreen.png')
		mainLoop = False
		
	if pygame.mouse.get_pressed()[0] == 1 and click1 == False and draw == True and pygame.mouse.get_pos()[0] in bt_buffer['x'] and pygame.mouse.get_pos()[1] in bt_buffer['y']:
		activebutton = True
		cropped_img = imgPIL.crop(click1_pose+mouse_pose)
		cropped_img.save('/tmp/augscreen.png')
		os.system('xclip -selection clipboard -t image/png -i /tmp/augscreen.png;rm /tmp/augscreen.png')
		mainLoop = False

	if pygame.mouse.get_pressed()[0] == 1 and activebutton == False:
		draw = True
		mouse_pose = pygame.mouse.get_pos()

	if pygame.mouse.get_pressed()[0] == 1 and click1==False and activebutton == False:
		click1_pose = mouse_pose
		click1 = True
		mouse_pose = click1_pose
	if pygame.mouse.get_pressed()[0] == 0 and click1==True:
		click1 = False
	
	if pygame.mouse.get_pos()[0] + 90 > w or pygame.mouse.get_pos()[1] + 55 > h:
		fullscreen_bt = True
	else:
		fullscreen_bt = False
	
	if click1_pose[1] - 25 < 0:
		fullscreen_coords = True
	else:
		fullscreen_coords = False
	
	if draw:
		pygame.draw.circle(screen,[74,74,74], click1_pose,5)
		pygame.draw.line(screen, [74,74,74], click1_pose, [mouse_pose[0],click1_pose[1]])
		pygame.draw.line(screen, [74,74,74], [mouse_pose[0],click1_pose[1]], mouse_pose)
		pygame.draw.line(screen, [74,74,74], click1_pose, [click1_pose[0],mouse_pose[1]])
		pygame.draw.line(screen, [74,74,74], [click1_pose[0],mouse_pose[1]], mouse_pose)
		
		if fullscreen_coords:
			pygame.draw.rect(screen, [74,74,74], [click1_pose[0],click1_pose[1]+10,90,25])
			font = pygame.font.Font(None, 25)
			text = font.render(str(mouse_pose[0]-click1_pose[0]).replace('-','')+'x'+str(mouse_pose[1]-click1_pose[1]).replace('-',''),True,[255,255,255])
			screen.blit(text, [click1_pose[0],click1_pose[1]+10])
		else:
			pygame.draw.rect(screen, [74,74,74], [click1_pose[0],click1_pose[1]-30,90,25])
			font = pygame.font.Font(None, 25)
			text = font.render(str(mouse_pose[0]-click1_pose[0]).replace('-','')+'x'+str(mouse_pose[1]-click1_pose[1]).replace('-',''),True,[255,255,255])
			screen.blit(text, [click1_pose[0],click1_pose[1]-28])
		
		if fullscreen_bt:
			pygame.draw.rect(screen, [74,74,74], [mouse_pose[0]-70-90,mouse_pose[1]-30,60,25])
			font = pygame.font.Font(None, 25)
			text = font.render("буфер",True,[255,255,255])
			screen.blit(text, [mouse_pose[0]-70-90,mouse_pose[1]-30])
			bt_buffer['x'] = range(mouse_pose[0]-70-90,mouse_pose[0]-70-90+60)
			bt_buffer['y'] = range(mouse_pose[1]-30,mouse_pose[1]-30+25)
			
			pygame.draw.rect(screen, [74,74,74], [mouse_pose[0]-95,mouse_pose[1]-30,90,25])
			font = pygame.font.Font(None, 25)
			text = font.render("сохранить",True,[255,255,255])
			screen.blit(text, [mouse_pose[0]-95,mouse_pose[1]-30])
			bt_save['x'] = range(mouse_pose[0]-95,mouse_pose[0]-95+90)
			bt_save['y'] = range(mouse_pose[1]-30,mouse_pose[1]+30+25)	
		else:			
			pygame.draw.rect(screen, [74,74,74], [mouse_pose[0]+10,mouse_pose[1],60,25])
			font = pygame.font.Font(None, 25)
			text = font.render("буфер",True,[255,255,255])
			screen.blit(text, [mouse_pose[0]+10,mouse_pose[1]])
			bt_buffer['x'] = range(mouse_pose[0]+10,mouse_pose[0]+10+60)
			bt_buffer['y'] = range(mouse_pose[1],mouse_pose[1]+60)
			
			pygame.draw.rect(screen, [74,74,74], [mouse_pose[0]+10,mouse_pose[1]+30,90,25])
			font = pygame.font.Font(None, 25)
			text = font.render("сохранить",True,[255,255,255])
			screen.blit(text, [mouse_pose[0]+10,mouse_pose[1]+30])
			bt_save['x'] = range(mouse_pose[0]+10,mouse_pose[0]+10+90)
			bt_save['y'] = range(mouse_pose[1]+30,mouse_pose[1]+30+25)
	
		pygame.draw.circle(screen,[74,74,74],mouse_pose,5)
	
		
	pygame.display.update()
	time.sleep(0.01)
pygame.quit()

