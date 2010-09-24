import pygame

class Entity:
    Entities = []

    def getNextFrame(self):
        temp = self.currentAnimimation
        if self.vx == 0 and self.vy == 0:
            self.currentAnimimation = self.entityType.animations['idle']
        elif self.vx != 0 and self.vy == 0:
            try:
                self.currentAnimimation = self.entityType.animations['move']
            except KeyError:
                self.currentAnimimation = self.entityType.animations['idle']
        elif self.vx == 0 and self.vy != 0:
            try:
                self.currentAnimimation = self.entityType.animations['jump']
            except KeyError:
                self.currentAnimimation = self.entityType.animations['idle']
        else:
            try:
                self.currentAnimimation = self.entityType.animations['jumpdiag']
            except KeyError:
                self.currentAnimimation = self.entityType.animations['idle']
        if temp != self.currentAnimimation:
            self.currentAnimimationFrame = -1
        self.currentAnimimationFrame += 1
        if self.currentAnimimationFrame > len(self.currentAnimimation.frame):
            self.currentAnimimationFrame = 0
        if self.flipped:
            self.curFrame = pygame.transform.flip(self.currentAnimimation.frame[self.currentAnimimationFrame], 1, 0)
            return self.curFrame
        else:
            self.curFrame = self.currentAnimimation.frame[self.currentAnimimationFrame]
            return self.curFrame

    def __init__(self, position, whichType):
        Entity.Entities.append(self)
        self.flipped = True

        self.position = position
        self.velocity = (0, 0)
        self.acceleration = (0, 0)

        self.entityType = whichType
        self.currentAnimimation = self.entityType.animations['idle']
        self.currentAnimationFrame = -1
        self.currentFrame = None

        self.falling = True
        self.jumping = False
        self.jumpCounter = 0
        self.flying = False
        self.flyCounter = 0
