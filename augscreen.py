#!/usr/bin/python3
import os, time, sys
from PIL import Image
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *

if 'save' in sys.argv:
    save = True
else:
    save = False
os.system('import -window root /tmp/augscreen.png')
imgPIL = Image.open('/tmp/augscreen.png')
w,h = imgPIL.size
pygame.init()

#screen = pygame.display.set_mode((w,h),0,32)
screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)
#pygame.display.toggle_fullscreen()

img = pygame.image.load('/tmp/augscreen.png')
newSurf = pygame.Surface((w,h))
newSurf.blit(img, (0,0))

mainLoop = True
click1 = False
click2 = False
while mainLoop:
	for event in pygame.event.get():
		if event.type == QUIT:
				mainLoop = False
	screen.fill((255,255,255))
	screen.blit(newSurf, (0,0))
	mouse_pose = pygame.mouse.get_pos()
	if pygame.mouse.get_pressed()[0] == 1 and click1==False:
		print('1 click on',mouse_pose)
		click1_pose = mouse_pose
		click1 = True
	if pygame.mouse.get_pressed()[2] == 1 and click1:
		print('2 click on',mouse_pose)
		click2_pose = mouse_pose
		click2 = True
	if click1 and click2 != True:
		pygame.draw.circle(screen,[255,0,0], click1_pose,5)
		pygame.draw.line(screen, [255,0,0], click1_pose, [mouse_pose[0],click1_pose[1]])
		pygame.draw.line(screen, [255,0,0], [mouse_pose[0],click1_pose[1]], mouse_pose)
		pygame.draw.line(screen, [255,0,0], click1_pose, [click1_pose[0],mouse_pose[1]])
		pygame.draw.line(screen, [255,0,0], [click1_pose[0],mouse_pose[1]], mouse_pose)
		pygame.draw.circle(screen,[255,0,0],mouse_pose,5)
	if click1 and click2:
		pygame.draw.circle(screen,[255,0,0], click1_pose,5)
		pygame.draw.line(screen, [255,0,0], click1_pose, [click2_pose[0],click1_pose[1]])
		pygame.draw.line(screen, [255,0,0], [click2_pose[0],click1_pose[1]], click2_pose)
		pygame.draw.line(screen, [255,0,0], click1_pose, [click1_pose[0],click2_pose[1]])
		pygame.draw.line(screen, [255,0,0], [click1_pose[0],click2_pose[1]], click2_pose)
		pygame.draw.circle(screen,[255,0,0],click2_pose,5)
	pygame.display.update()
	if click1 and click2 and pygame.mouse.get_pressed()[0] == 1:
		mainLoop = False
		pygame.quit()
	time.sleep(0.005)
pygame.quit()
print('Click1: ',click1_pose,'\nClick2: ',click2_pose)
cropped_img = imgPIL.crop(click1_pose+click2_pose)
if save:
    if 'Изображения' in os.listdir(os.getcwd()):
        cropped_img.save(os.getcwd()+'/Изображения/augscreen.png')
    else:
        cropped_img.save(os.getcwd()+'/Pictures/augscreen.png')
else:
    cropped_img.save('/tmp/augscreen.png')
    os.system('xclip -selection clipboard -t image/png -i /tmp/augscreen.png;rm /tmp/augscreen.png')
print('Сохранено в буфер')
