import pygame
#import pygame.camera

import picamera
import io

from pygame.locals import *

from . import ui, camera, lamp

class MenuGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 172)
    text =  "Menu"

class MenuZoom(ui.Button):
    x, y, w, h = (684, 32, 110, 48)
    text = "Zoom"
    def action(self):
        self.app.widget = 'zoom'

class MenuLamp(ui.Button):
    x, y, w, h = (684, 84, 110, 48)
    text = "Lamp"
    def action(self):
        self.app.widget = 'lamp'

class MenuCamera(ui.Button):
    x, y, w, h = (684, 136, 110, 48)
    text = "Camera"
    def action(self):
        self.app.widget = 'camera'

class ZoomGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 172)
    text =  "Zoom"

class ZoomIn(ui.Button):
    x, y, w, h = (684, 32, 110, 48)
    text = "+"

    def action(self):
        self.app.cam.zoom_in(0.05)

class ZoomOut(ui.Button):
    x, y, w, h = (684, 84, 110, 48)
    text = "-"

    def action(self):
        self.app.cam.zoom_out(0.05)

class ZoomBack(ui.Button):
    x, y, w, h = (684, 136, 110, 48)
    text = "Back"

    def action(self):
        self.app.widget = 'menu'

class LampGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 330)
    text =  "Lamp"

class LampOn(ui.Button):
    x, y, w, h = (684, 32, 110, 48)
    text = "On"

    def action(self):
        self.app.lamp.on()

class LampOff(ui.Button):
    x, y, w, h = (684, 84, 110, 48)
    text = "Off"

    def action(self):
        self.app.lamp.off()

class LampBrightDown(ui.Button):
    x, y, w, h = (684, 136, 48, 48)
    text = "-"

    def action(self):
        brightness = self.app.lamp.brightness
        if brightness > 10:
            self.app.lamp.setBrightness(brightness - 10)

class LampBrightUp(ui.Button):
    x, y, w, h = (745, 136, 48, 48)
    text = "+"

    def action(self):
        brightness = self.app.lamp.brightness
        if brightness <= 90:
            self.app.lamp.setBrightness(brightness + 10)

class LampRInc(ui.Button):
    x, y, w, h = (684, 188, 32, 48)
    text = "^"
    def action(self):
        if self.app.lamp_color[0] < 244:
            self.app.lamp_color[0] += 10

        self.fill = (self.app.lamp_color[0], 0, 0)
        self.app.lamp.fill(*self.app.lamp_color)

class LampGInc(ui.Button):
    x, y, w, h = (722, 188, 32, 48)
    text = "^"
    def action(self):
        if self.app.lamp_color[1] < 244:
            self.app.lamp_color[1] += 10
        self.fill = (0, self.app.lamp_color[1], 0)
        self.app.lamp.fill(*self.app.lamp_color)

class LampBInc(ui.Button):
    x, y, w, h = (760, 188, 32, 48)
    text = "^"
    def action(self):
        if self.app.lamp_color[2] < 244:
            self.app.lamp_color[2] += 10
        self.fill = (0, 0, self.app.lamp_color[2])
        self.app.lamp.fill(*self.app.lamp_color)

class LampRDec(ui.Button):
    x, y, w, h = (684, 240, 32, 48)
    text = "v"
    def action(self):
        if self.app.lamp_color[0] > 10:
            self.app.lamp_color[0] -= 10
        self.fill = (self.app.lamp_color[0], 0, 0)
        self.app.lamp.fill(*self.app.lamp_color)

class LampGDec(ui.Button):
    x, y, w, h = (722, 240, 32, 48)
    text = "v"
    def action(self):
        if self.app.lamp_color[1] > 10:
            self.app.lamp_color[1] -= 10
        self.fill = (0, self.app.lamp_color[1], 0)
        self.app.lamp.fill(*self.app.lamp_color)

class LampBDec(ui.Button):
    x, y, w, h = (760, 240, 32, 48)
    text = "v"
    def action(self):
        if self.app.lamp_color[2] > 10:
            self.app.lamp_color[2] -= 10
        self.fill = (0, 0, self.app.lamp_color[2])
        self.app.lamp.fill(*self.app.lamp_color)

class LampBack(ui.Button):
    x, y, w, h = (684, 292, 110, 48)
    text = "Back"

    def action(self):
        self.app.widget = 'menu'

class CameraGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 120)
    text =  "Camera"

class CameraSave(ui.Button):
    x, y, w, h = (684, 32, 110, 48)
    text = "Save"

    def action(self):
        self.app.cam.save()

class CameraBack(ui.Button):
    x, y, w, h = (684, 84, 110, 48)
    text = "Back"

    def action(self):
        self.app.widget = 'menu'


class App(object):
    def __init__(self):
        pygame.display.init()
        pygame.font.init()

        self.display_setup()

        self.lamp = lamp.Lamp()

        self.cam = camera.Camera()

        self.clock = pygame.time.Clock()

        self.special = False

        self.button_font = pygame.font.SysFont("DejaVuSans", 12)

        self.lamp_color = [128, 128, 128]

        self.widgets = {
            'menu': [
                MenuGroup(self.button_font),
                MenuZoom(self, self.button_font),
                MenuLamp(self, self.button_font),
                MenuCamera(self, self.button_font)
            ],
            'zoom': [
                ZoomGroup(self.button_font),
                ZoomIn(self, self.button_font),
                ZoomOut(self, self.button_font),
                ZoomBack(self, self.button_font),
            ],
            'lamp': [
                LampGroup(self.button_font),
                LampOn(self, self.button_font),
                LampOff(self, self.button_font),

                LampBrightDown(self, self.button_font),
                LampBrightUp(self, self.button_font),

                LampRInc(self, self.button_font),
                LampGInc(self, self.button_font),
                LampBInc(self, self.button_font),

                LampRDec(self, self.button_font),
                LampGDec(self, self.button_font),
                LampBDec(self, self.button_font),

                LampBack(self, self.button_font)
            ],
            'camera': [
                CameraGroup(self.button_font),
                CameraSave(self, self.button_font),
                CameraBack(self, self.button_font)
            ]
        }

        self.widget = 'menu'

        self.run = True

        h = 0

        while self.run:
            self.surface.fill(pygame.Color(0, 0, 0))
            if self.special:
                h += 0.002
                if h > 1:
                    h = 0

                self.lamp.fillHSV(h, 1.0, 1.0)


            self.loop()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def toggle_special(self):
        self.special = not self.special

    def display_setup(self):
        pygame.display.set_caption("Picroscope")
        self.display = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.surface = pygame.display.get_surface()

    def exit(self):
        self.run = False

    def loop(self):
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                self.exit()
                return

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos

                for widget in self.widgets[self.widget]:
                    if hasattr(widget, 'inside') and widget.inside(x, y):
                        widget.action()

        for widget in self.widgets[self.widget]:
            widget.draw(self.surface)

