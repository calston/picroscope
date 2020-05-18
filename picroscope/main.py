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
    x, y, w, h = (680, 16, 119, 380)
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


class LampBright(ui.Value):
    x, y, w, h = (684, 136, 110, 48)
    button_w = 32
    text = "L"

    def action(self):
        if self.button == 0:
            if self.value > 10:
                self.value -= 10
        else:
            if self.value < 100:
                self.value += 10

        self.app.lamp.setBrightness(self.value)

class LampR(ui.Value):
    x, y, w, h = (684, 188, 110, 48)
    button_w = 32
    text = "R"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.fill = (self.value, 0, 0)

    def action(self):
        if self.button == 1:
            if self.value < 254:
                self.value += 10
        else:
            if self.value > 10:
                self.value -= 10

        self.app.lamp_color[0] = self.value

        self.fill = (self.app.lamp_color[0], 0, 0)
        self.app.lamp.fill(*self.app.lamp_color)


class LampG(ui.Value):
    x, y, w, h = (684, 240, 110, 48)
    button_w = 32
    text = "G"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.fill = (0, self.value, 0)

    def action(self):
        if self.button == 1:
            if self.value < 254:
                self.value += 10
        else:
            if self.value > 10:
                self.value -= 10

        self.app.lamp_color[1] = self.value
        self.fill = (0, self.app.lamp_color[1], 0)
        self.app.lamp.fill(*self.app.lamp_color)


class LampB(ui.Value):
    x, y, w, h = (684, 292, 110, 48)
    button_w = 32
    text = "B"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.fill = (0, 0, self.value)

    def action(self):
        if self.button == 1:
            if self.value < 254:
                self.value += 10
        else:
            if self.value > 10:
                self.value -= 10

        self.app.lamp_color[2] = self.value
        self.fill = (0, 0, self.app.lamp_color[2])
        self.app.lamp.fill(*self.app.lamp_color)


class LampBack(ui.Button):
    x, y, w, h = (684, 344, 110, 48)
    text = "Back"

    def action(self):
        self.app.widget = 'menu'


class CameraGroup(ui.Group):
    x, y, w, h = (680, 16, 119, 380)
    text =  "Camera"


class CameraISO(ui.Value):
    x, y, w, h = (684, 32, 110, 48)
    button_w = 32
    text = "ISO"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.camera = self.app.cam.camera
        self.iso_value = self.camera.iso
        self.iso_list = ['AUTO', 100, 200, 320, 400, 500, 640, 800]
        if self.iso_value in self.iso_list:
            self.value = self.iso_list[self.iso_value]
        else:
            self.value = 'AUTO'

    def action(self):
        if self.button == 1:
            if self.iso_value < len(self.iso_list) - 1:
                self.iso_value += 1
        else:
            if self.iso_value > 0:
                self.iso_value -= 1

        self.value = self.iso_list[self.iso_value]
        if self.iso_value > 0:
            self.camera.iso = self.iso_list[self.iso_value]
        else:
            self.camera.iso = 0


class CameraMeter(ui.Value):
    x, y, w, h = (684, 84, 110, 48)
    button_w = 32
    text = "Meter"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.camera = self.app.cam.camera
        self.l_value = 0
        self.value_list = ['Average', 'Spot', 'Backlit', 'Matrix']
        self.value = self.value_list[self.l_value]

    def action(self):
        if self.button == 1:
            if self.l_value < len(self.value_list) - 1:
                self.l_value += 1
        else:
            if self.l_value > 0:
                self.l_value -= 1

        self.value = self.value_list[self.l_value]
        self.camera.meter_mode = self.value_list[self.l_value].lower()


class CameraSharpness(ui.Value):
    x, y, w, h = (684, 136, 110, 48)
    button_w = 32
    text = "Sharp"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.camera = self.app.cam.camera

    def action(self):
        if self.button == 1:
            if self.value < 100:
                self.value += 1
        else:
            if self.value > -100:
                self.value -= 1

        self.camera.sharpness = self.value


class CameraStab(ui.Button):
    x, y, w, h = (684, 188, 110, 48)
    text = "Stabilize"

    def __init__(self, *a, **kw):
        ui.Button.__init__(self, *a, **kw)
        self.camera = self.app.cam.camera
        self.fill = (0, 0, 0)

    def action(self):
        if self.camera.video_stabilization:
            self.camera.video_stabilization = False
            self.fill = (0, 0, 0)
        else:
            self.camera.video_stabilization = True
            self.fill = (64, 64, 64)


class CameraMode(ui.Value):
    x, y, w, h = (684, 240, 110, 48)
    button_w = 32
    text = "Mode"

    def __init__(self, *a, **kw):
        ui.Value.__init__(self, *a, **kw)
        self.camera = self.app.cam.camera

        self.modes = [
            ('12MP', (4056, 3040)),
            ('4K', (4056, 2288)),
            ('3MP', (2028, 1520)),
            ('1080p', (2028, 1128))
        ]
        self.sel_mode = 0
        self.value = '12Mp'

    def action(self):
        if self.button == 1:
            if self.sel_mode < 3:
                self.sel_mode += 1
        else:
            if self.sel_mode > 0:
                self.sel_mode -= 1

        self.value = self.modes[self.sel_mode][0]
        self.camera.resolution = self.modes[self.sel_mode][1]
        self.app.cam.set_zoom()


class CameraSave(ui.Button):
    x, y, w, h = (684, 292, 110, 48)
    text = "Save"

    def action(self):
        self.app.cam.save()


class CameraBack(ui.Button):
    x, y, w, h = (684, 344, 110, 48)
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

        self.widget_font = pygame.font.SysFont("DejaVuSans", 12)

        self.lamp_color = [254, 254, 174]

        self.widgets = {
            'menu': [
                MenuGroup(self),
                MenuZoom(self),
                MenuLamp(self),
                MenuCamera(self)
            ],
            'zoom': [
                ZoomGroup(self),
                ZoomIn(self),
                ZoomOut(self),
                ZoomBack(self),
            ],
            'lamp': [
                LampGroup(self),
                LampOn(self),
                LampOff(self),

                LampBright(self, 50),

                LampR(self, self.lamp_color[0]),
                LampG(self, self.lamp_color[1]),
                LampB(self, self.lamp_color[2]),

                LampBack(self)
            ],
            'camera': [
                CameraGroup(self),
                CameraISO(self),
                CameraMeter(self),
                CameraSharpness(self),
                CameraStab(self),
                CameraMode(self),
                CameraSave(self),
                CameraBack(self)
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

