"""

The Player is the Entity that the player controls.

"""

from Entity import Entity

class Player(Entity):

    FlyAcceleration = 0.52
    JumpInitialVelocity = 10
    HorizontalMoveSpeed = 3

    MaxFlyLength = 16

    MovingLeft, MovingRight, NotMoving = range(3)

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        self.currentAnimation = self.objectType.animations['idle']
        if self.moveState != Player.NotMoving:
            self.currentAnimation = self.objectType.animations['move']

    def flying(self, isFlying):
        """
        Starts/Stops the player's Jetpack.        
        """

        if (not self.isFlying and isFlying and self.flyCounter <= Player.MaxFlyLength):
            self.isFlying = True
            self.acceleration[1] -= Player.FlyAcceleration
        elif (self.isFlying and not isFlying):
            self.isFlying = False
            self.acceleration[1] += Player.FlyAcceleration
        elif (self.isFlying and isFlying):
            self.flyCounter += 1
            if self.flyCounter > Player.MaxFlyLength:
                self.isFlying = False
                self.acceleration[1] += Player.FlyAcceleration

    def jumping(self, isJumping):
        """
        Starts/Stops the player's jump
        """

        if (isJumping and not self.isJumping and self.velocity[1] == 0):
            self.isJumping = True
            self.velocity[1] -= Player.JumpInitialVelocity
        elif (not isJumping and self.isJumping):
            self.isJumping = False
            if (self.velocity[1] < 0 and not self.isFlying):
                self.velocity[1] = 0

    def running(self, toRight, isRunning):
        """
        Starts/Stops the player's horizontal movement.
        """

        if not isRunning:
            self.velocity[0] = 0
            self.moveState = Player.NotMoving
        else:
            self.velocity[0] = ((Player.HorizontalMoveSpeed) if toRight else (-Player.HorizontalMoveSpeed))
            if (self.velocity[0] > 0):
                self.moveState = Player.MovingRight
                self.flipped = False
            elif (self.velocity[0] < 0):
                self.moveState = Player.MovingLeft
                self.flipped = True

    def onLand(self):
        """
        Called when the player lands on ground of some sort
        """
        Entity.onLand(self)
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0

    def __init__(self, whichType, position = [0, 0], flipped = False):
        Entity.__init__(self, whichType, position = position, flipped = flipped)
        self.moveState = Player.NotMoving
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0
