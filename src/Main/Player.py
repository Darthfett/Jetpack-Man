"""

The Player is the Entity that the player controls.

"""

from Entity import Entity

class Player(Entity):

    FlyAcceleration = 0.51
    JumpInitialVelocity = 9
    HorizontalMoveSpeed = 0.7
    MaxHorizontalMoveSpeed = 4

    MaxFlyLength = 64

    MovingLeft, MovingRight, NotMoving = range(3)

    def getNextFrame(self):
        """
        Calculates the current animation.
        """
        if self.blink:
            self.draw = not self.draw
        self.currentAnimation = self.objectType.animations['idle']
        if self.moveState != Player.NotMoving:
            self.currentAnimation = self.objectType.animations['move']
        if self.isFlying:
            self.currentAnimation = self.objectType.animations['fly']

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
            self.flyCounter += 0.5 + abs(min(0, self.velocity[1] / 2))
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
            if self.velocity[0] != 0 and abs(self.velocity[0]) < Player.HorizontalMoveSpeed:
                self.velocity[0] = 0
            elif self.velocity[0] >= Player.HorizontalMoveSpeed:
                self.velocity[0] -= Player.HorizontalMoveSpeed
            elif abs(self.velocity[0]) >= Player.HorizontalMoveSpeed:
                self.velocity[0] += Player.HorizontalMoveSpeed
            self.moveState = Player.NotMoving
        else:
            if toRight:
                self.velocity[0] = min(self.velocity[0] + Player.HorizontalMoveSpeed,Player.MaxHorizontalMoveSpeed)
            else:
                self.velocity[0] = max(self.velocity[0] - Player.HorizontalMoveSpeed,-Player.MaxHorizontalMoveSpeed)
            self.flipped = not toRight
            self.moveState = Player.MovingRight if toRight else Player.MovingLeft

    def onLand(self):
        """
        Called when the player lands on ground of some sort
        """
        Entity.onLand(self)
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0

    def __init__(self, whichType, position = [0, 0], flipped = False, blink = False):
        Entity.__init__(self, whichType, position = position, flipped = flipped)
        self.blink = blink
        self.moveState = Player.NotMoving
        self.isJumping = False
        self.isFlying = False
        self.flyCounter = 0
