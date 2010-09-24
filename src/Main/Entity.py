import pygame

class Entity:
    Entities = []

    def getNextFrame(self):
        temp = self.currentAnimation
        self.currentAnimation = self.entityType.animations['idle']
#        if (self.velocity == (0, 0)):
#            self.currentAnimation = self.entityType.animations['idle']
#        elif self.velocity[0] != 0 and self.velocity[1] == 0:
#            try:
#                self.currentAnimation = self.entityType.animations['move']
#            except KeyError:
#                self.currentAnimation = self.entityType.animations['idle']
#        elif self.velocity[0] == 0 and self.velocity[1] != 0:
#            try:
#                self.currentAnimation = self.entityType.animations['jump']
#            except KeyError:
#                self.currentAnimation = self.entityType.animations['idle']
#        else:
#            try:
#                self.currentAnimation = self.entityType.animations['jumpdiag']
#            except KeyError:
#                self.currentAnimation = self.entityType.animations['idle']
        if temp != self.currentAnimation:
            self.currentAnimationFrame = -1
        self.currentAnimationFrame += 1
        if self.currentAnimationFrame >= len(self.currentAnimation.frame):
            self.currentAnimationFrame = 0
        if self.flipped:
            self.curFrame = pygame.transform.flip(self.currentAnimation.frame[self.currentAnimationFrame], 1, 0)
            return self.curFrame
        else:
            self.curFrame = self.currentAnimation.frame[self.currentAnimationFrame]
            return self.curFrame

    def __init__(self, whichType):
        Entity.Entities.append(self)
        self.flipped = True

        self.position = [0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

        self.entityType = whichType
        self.currentAnimation = self.entityType.animations['idle']
        self.currentAnimationFrame = -1
        self.currentFrame = self.getNextFrame()

        self.falling = True
        self.jumping = False
        self.jumpCounter = 0
        self.flying = False
        self.flyCounter = 0
