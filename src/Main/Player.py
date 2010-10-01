"""

The Player is the Entity that the player controls.

"""

from Entity import Entity

class Player(Entity):

    FlyAcceleration = 0.6
    JumpInitialVelocity = 10
    HorizontalMoveSpeed = 3

    MaxJumpLength = 16

    MaxFlyLength = 16

    def flying(self, isFlying):
        """
        Starts/Stops the player's jetpack.        
        """
        if (not self.isFlying and isFlying):
            print "DEBUG: Player started Flying"
            self.isFlying = True
            self.isFalling = True
            self.acceleration[1] -= Player.FlyAcceleration
        elif (self.isFlying and not isFlying):
            print "DEBUG: Player stopped Flying"
            self.isFlying = False
            self.acceleration[1] += Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """
        if (isJumping and not self.isJumping and not self.isFalling):
            print "DEBUG: Player starting Jumping"
            self.isJumping = True
            self.isFalling = True
            self.velocity[1] -= Player.JumpInitialVelocity
        elif (not isJumping and self.isJumping):
            print "DEBUG: Player stopped Jumping"
            self.isJumping = False
            if (self.velocity[1] < 0 and not self.isFlying):
                self.velocity[1] = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """
        if not isRunning:
            self.velocity[0] = 0
        else:
            self.velocity[0] = ((Player.HorizontalMoveSpeed) if toRight else (-Player.HorizontalMoveSpeed))
            if (self.velocity[0] > 0):
                self.flipped = False
            elif (self.velocity[0] < 0):
                self.flipped = True

    def onLand(self):
        """
        Called when the player lands on ground of some sort
        """
        print "DEBUG: Player Landing"
        self.isJumping = False
        self.isFlying = False
        self.isFalling = False
        self.velocity[1] = 0
        self.acceleration[1] = 0

    def __init__(self, whichType):
        Entity.__init__(self, whichType)
        self.isFalling = True
        self.isJumping = False
        self.jumpCounter = Player.MaxFlyLength
        self.isFlying = False
        self.flyCounter = 0
