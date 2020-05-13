import picamera
import os

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()

        self.camera.resolution = (4056, 3040)
        self.camera.rotation=180

        self.camera.start_preview()

        self.camera.preview.fullscreen = False

        self.camera.preview.window = (0, 0, 680, 480)

        self.zoom_val = 1.0
        self.set_zoom()

    def resize(self, x, y, w, h):
        self.camera.preview.window = (x, y, w, h)

    def set_zoom(self):
        rw, rh = self.camera.resolution

        cpx = ((rw/2.0) - ((self.zoom_val*rw)/2.0))/rw
        cpy = ((rh/2.0) - ((self.zoom_val*rh)/2.0))/rh
        self.camera.zoom = (cpx, cpy, self.zoom_val, self.zoom_val)

    def zoom_out(self, amount):
        if self.zoom_val < 1:
            self.zoom_val += amount
            if self.zoom_val > 1:
                self.zoom_val = 1
            self.set_zoom()

    def zoom_in(self, amount):
        if self.zoom_val > 0.03:
            self.zoom_val -= amount
            if self.zoom_val < 0.03:
                self.zoom_val = 0.03
            self.set_zoom()

    def save(self, path=os.path.expanduser('~/Pictures')):
        image_numbers = [int(i.split('.')[0].split('_')[-1])
            for i in os.listdir(path) if i.startswith('IMG_')]

        if not image_numbers:
            image_numbers = [0]

        next_image = max(image_numbers) + 1

        file_name = "IMG_%04d.png" % next_image
        self.camera.capture(os.path.join(path, file_name))
