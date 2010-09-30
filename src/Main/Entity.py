"""

An Entity is an object that is drawn to the screen.

It can have animations, as well as position, velocity, and acceleration.

"""

import pygame

class Entity:
    Entities = []

    def getNextFrame(self):
        temp = self.currentAnimation
        self.currentAnimation = self.entityType.animations['idle']
        if (self.velocity[0] != 0):
            self.currentAnimation = self.entityType.animations['move']

        # Possibly here, determine animation

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
