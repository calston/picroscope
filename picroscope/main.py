import pygame
#import pygame.camera

import picamera
import io

from pygame.locals import *

from . import ui, camera

class ZoomGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 120)
    text =  "Zoom"

class ZoomIn(ui.Button):
    x, y, w, h = (684, 32, 110, 48)
    text = "+"

    def __init__(self, font, cam):
        self.font = font
        self.cam = cam

    def action(self):
        self.cam.zoom_in(0.05)

class ZoomOut(ui.Button):
    x, y, w, h = (684, 84, 110, 48)
    text = "-"

    def __init__(self, font, cam):
        self.font = font
        self.cam = cam

    def action(self):
        self.cam.zoom_out(0.05)

class App(object):
    def __init__(self):
        pygame.init()

        self.display_setup()

        self.cam = camera.Camera()

        self.clock = pygame.time.Clock()

        self.button_font = pygame.font.SysFont("DejaVuSans", 12)

        self.widgets = [
            ZoomGroup(self.button_font),
            ZoomIn(self.button_font, self.cam),
            ZoomOut(self.button_font, self.cam)
        ]

        self.run = True

        while self.run:
            self.loop()

            #pygame.display.blit(self.surface, )
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def display_setup(self):
        pygame.display.set_caption("Picroscope")
        self.display = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.surface = pygame.display.get_surface()

        #print(pygame.display.Info())
        print(self.surface.get_size())

    def exit(self):
        self.run = False

    def loop(self):
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                self.exit()
                return

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos

                for widget in self.widgets:
                    if hasattr(widget, 'inside') and widget.inside(x, y):
                        widget.action()

        for widget in self.widgets:
            widget.draw(self.surface)

