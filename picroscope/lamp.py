import serial
import colorsys
import os

CMD_BRIGHTNESS = 1
CMD_SET_PIXEL = 2
CMD_PUSH_PIXEL = 3
CMD_SET_PIXEL_HSV = 20
CMD_PUSH_PIXEL_HSV = 30
CMD_CLEAR = 4
CMD_FILL = 5


class Lamp(object):
    def __init__(self, device='/dev/ttyUSB0'):
        if os.path.exists(device):
            self.serial = serial.Serial(device, 115200)
            self.serial.write(b'4\n')
        else:
            self.serial = None

        self.brightness = 20

    def send_command(self, command, *args):
        self.serial.write(bytes("%s.%s\n" % (command, '.'.join([str(i) for i in args])), 'ascii'))

    def close(self):
        self.serial.close()

    def off(self):
        self.send_command(CMD_CLEAR)

    def on(self):
        self.send_command(CMD_FILL, 254, 254, 254)

    def fill(self, r, g, b):
        self.send_command(CMD_FILL, r, g, b)

    def fillHSV(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.send_command(CMD_FILL, int(r*254), int(g*254), int(b*254))

    def pushHSV(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.send_command(CMD_PUSH_PIXEL, int(r*254), int(g*254), int(b*254))

    def setBrightness(self, value):
        self.brightness = value
        self.send_command(CMD_BRIGHTNESS, value)
