import pygame

class Widget:
    pass

class Group(Widget):
    def __init__(self, font):
        self.font = font

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
    def __init__(self, font):
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(255, 255,255),
            (self.x, self.y, self.w, self.h), 2)

        text = self.font.render(self.text, False, pygame.Color(255, 255,255))

        tw, th = self.font.size(self.text)
        
        surface.blit(text, (self.x+((self.w/2) - (tw/2)), self.y+((self.h/2) - (th/2))))

    def inside(self, x, y):
        inx = (x > self.x) and (y < (self.x+self.w))
        iny = (y > self.y) and (y < (self.y+self.h))

        if inx and iny:
            return True
        else:
            return False

    def action(self):
        pass
