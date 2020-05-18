import pygame

class Widget:
    def __init__(self, app):
        self.app = app
        self.font = self.app.widget_font
    pass

class Group(Widget):
    def draw(self, surface):
        text = self.font.render(self.text, False, pygame.Color(255, 255,255))

        tw, th = self.font.size(self.text)
        
        margin = 8

        pygame.draw.lines(surface, pygame.Color(255, 255,255), False, (
            (self.x+margin, self.y+(th/2)),
            (self.x, self.y+(th/2)),
            (self.x, self.y+self.h),
            (self.x+self.w, self.y+self.h),
            (self.x+self.w, self.y+(th/2)),
            (self.x+margin+8+tw, self.y+(th/2))
        ))

        surface.blit(text, (self.x + margin + 4, self.y))

class Button(Widget):
    def __init__(self, app):
        Widget.__init__(self, app)
        self.fill = (64, 64, 64)

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(*self.fill),
            (self.x, self.y, self.w, self.h))

        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (self.x, self.y, self.w, self.h), 2)

        text = self.font.render(self.text, False, pygame.Color(255, 255,255))

        tw, th = self.font.size(self.text)
        
        surface.blit(text, (self.x+((self.w/2) - (tw/2)), self.y+((self.h/2) - (th/2))))

    def inside(self, x, y):
        inx = (x > self.x) and (x < (self.x+self.w))
        iny = (y > self.y) and (y < (self.y+self.h))

        if inx and iny:
            return True
        else:
            return False

    def action(self):
        pass

class Value(Widget):
    def __init__(self, app, value=0):
        Widget.__init__(self, app)
        self.fill = (64, 64, 64)
        self.value = value
        self.button = 0

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(*self.fill),
            (self.x, self.y, self.button_w, self.h))

        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (self.x, self.y, self.button_w, self.h), 2)

        pygame.draw.rect(surface, pygame.Color(*self.fill),
            (self.x + self.w - self.button_w, self.y, self.button_w, self.h))

        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (self.x + self.w - self.button_w, self.y, self.button_w, self.h), 2)

        tstr = "%s: %s" % (self.text, self.value)
        text = self.font.render(tstr, False, pygame.Color(255, 255,255))
        tw, th = self.font.size(tstr)

        if tw > (self.w - (2 * self.button_w)):
            text1 = self.font.render(self.text, False, pygame.Color(255, 255,255))
            tw1, _ = self.font.size(self.text)

            text2 = self.font.render(str(self.value), False, pygame.Color(255, 255,255))
            tw2, _ = self.font.size(str(self.value))

            bh = self.y + (self.h/2)

            surface.blit(text1, (self.x+((self.w/2) - (tw1/2)), bh - (th + 1)))
            surface.blit(text2, (self.x+((self.w/2) - (tw2/2)), bh + 1))
        else:
            surface.blit(text, (self.x+((self.w/2) - (tw/2)), self.y+((self.h/2) - (th/2))))
        
        arrow_left = self.font.render(u'←', False, pygame.Color(255, 255,255))
        surface.blit(arrow_left, (self.x+(self.button_w/2)-4, self.y+((self.h/2) - (th/2))))

        arrow_right = self.font.render(u'→', False, pygame.Color(255, 255,255))
        surface.blit(arrow_right, (self.x+self.w-(self.button_w/2)-4, self.y+((self.h/2) - (th/2))))

    def inside(self, x, y):
        inx = (x > self.x) and (x < (self.x + self.w))
        iny = (y > self.y) and (y < (self.y + self.h))

        if inx and iny:
            if (x < (self.x + self.button_w)):
                self.button = 0
            elif (x > (self.x + self.w - self.button_w)):
                self.button = 1
            else:
                return False
            return True
        else:
            return False

    def action(self):
        pass
