"""

The Player is the Entity that the player controls.

"""

from Entity import Entity

class Player(Entity):
    HorizontalMoveSpeed = 5

    JumpInitialVelocity = 12
    MaxJumpLength = 16

    MaxFlyLength = 16

    def fly(self, isStarting):
        if (not self.flying and isStarting):
            self.flying = True
            self.falling = True
            self.acceleration[1] -= 1
        elif (self.flying and not isStarting):
            self.flying = False
            self.acceleration[1] += 1
        print "DEBUG: Player Flying:", isStarting

    def jump(self, isStarting):
        print "DEBUG: Player Jumping:", isStarting
        if (isStarting and not self.falling):
            self.jumping = True
            self.jumpCounter = 0
            self.falling = True
            self.velocity[1] -= Player.JumpInitialVelocity
        elif (not isStarting):
            self.jumping = False
            if (self.velocity[1] < 0 and not self.flying):
                self.velocity[1] = 0

    def run(self, toRight):
        print "DEBUG: Player Running:", toRight
        self.velocity[0] += ((Player.HorizontalMoveSpeed) if toRight else (-Player.HorizontalMoveSpeed))
        if (self.velocity[0] > 0):
            self.flipped = False
        elif (self.velocity[0] < 0):
            self.flipped = True

    def onLand(self):
        print "DEBUG: Player Landing"
        self.jumping = False
        self.flying = False
        self.falling = False
        self.velocity[1] = 0
        self.acceleration[1] = 0

    def __init__(self, whichType):
        Entity.__init__(self, whichType)
        self.falling = True
        self.jumping = False
        self.jumpCounter = Player.MaxFlyLength
        self.flying = False
        self.flyCounter = 0
