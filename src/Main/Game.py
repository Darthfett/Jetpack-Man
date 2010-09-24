from Entity import Entity
from EntityType import EntityType
import pygame
import os

class Game:

    #Screen
    Screen = None
    ScreenWidth = 800
    ScreenHeight = 600
    FPSLimit = 100

    #Entities
    player = None

    #Controls
    Controls = {}
    ControlCount = 5
    MoveLeft, MoveRight, Jump, Duck, Fly = range(ControlCount)

    PlayerHorizontalMoveSpeed = 12

    #Physics
    Gravity = 4

    PlayerMaxJumpLength = 16
    PlayerMaxFlyLength = 16

    def drawFrame(self):
        Game.Screen.fill((0, 0, 0))
        for entity in Entity.Entities:
            Game.Screen.blit(entity.getNextFrame(), entity.position)

    def nextFrame(self):
        for entity in Entity.Entities:
            entity.position = [entity.position[i] + entity.velocity[i] for i in entity.position]
            entity.velocity = [entity.velocity[i] + entity.acceleration[i] for i in entity.position]
            if (entity.falling):
                entity.velocity[1] += Game.Gravity
            if (entity.flying):
                entity.flyCounter -= 2
            if (entity.flyCounter <= 0):
                if (entity.flying):
                    entity.acceleration[1] += 6
                entity.flying = False
            if (entity.jumping):
                entity.jumpcounter += 2
                if (entity.jumpcounter > Game.PlayerMaxJumpLength):
                    entity.jumping = False


            if (entity.position[1] + pygame.Surface.get_height(entity.currentFrame) > Game.ScreenWidth):
                entity.position[1] = Game.ScreenWidth - pygame.Surface.get_height(entity.currentFrame)
                entity.velocity[1] = 0
                entity.falling = False
                entity.flyCounter = Game.PlayerMaxFlyLength
                entity.acceleration[1] = 0
                entity.flying = False

    def registerInput(self, inputtype, press):
        Game.inputstate[inputtype] = press
        if (inputtype == Game.MoveLeft and press) or (inputtype == Game.MoveRight and not press):
            Game.Player.vx -= Game.PlayerHorizontalMoveSpeed
            if (inputtype == Game.MoveLeft) or (Game.Player.velocity[0] < 0):
                Game.Player.flipped = True
        elif (inputtype == Game.MoveLeft and not press) or (inputtype == Game.MoveRight and press):
            Game.Player.velocity += (Game.PlayerHorizontalMoveSpeed, 0)
            if (inputtype == Game.MoveRight) or (Game.Player.velocity[0] > 0):
                Game.Player.flipped = False
        elif (inputtype == Game.Jump and press and not Game.Player.falling):
            Game.Player.falling = True
            Game.Player.velocity[1] += 24
            Game.Player.jumping = True
        elif (inputtype == Game.Jump and not press):
            Game.Player.jumpcounter = 0
            Game.Player.jumping = False
            if (Game.Player.velocity[1] > 0 and not Game.Player.flying):
                Game.Player.velocity[1] = 0
        elif (inputtype == Game.Fly and press and not Game.Player.flying):
            Game.Player.flying = True
            Game.Player.acceleration[1] += 6
            Game.Player.falling = True
        elif (inputtype == Game.Fly and not press and Game.Player.flying):
            Game.Player.acceleration[1] -= 6
            Game.Player.flying = False

    def start(self):
        print "DEBUG: Starting Game"
        nextFrameTime = 0
        deltaFrameTime = 1000 / Game.FPSLimit
        try:
            while True:
                # Event Polling
                event = pygame.event.poll()
                while event:
                    if (event.type == pygame.QUIT or event.key == pygame.K_ESCAPE):
                        print "User Quit"
                        raise Exception("UserQuitException")

                    elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                        #Register Keypresses:
                        if Game.Controls.has_key(event.key):
                            self.registerInput(Game.Controls[event.key], event.type == pygame.KEYDOWN)

                    event = pygame.event.poll()

                currentTime = pygame.time.get_ticks()
                if ((nextFrameTime - currentTime) <= 0):
                    pygame.display.flip()

                    self.nextFrame()
                    self.drawFrame()
                    nextFrameTime = currentTime + deltaFrameTime

                pygame.time.delay(1)
        except Exception as inst:
            print 'Exception:'
            print '\t', type(inst)
            print '\t', inst
            pygame.quit()

    def initControls(self):
        print "DEBUG: Initializing Controls"
        Game.Controls[pygame.K_a] = Game.MoveLeft
        Game.Controls[pygame.K_d] = Game.MoveRight
        Game.Controls[pygame.K_w] = Game.Jump
        Game.Controls[pygame.K_s] = Game.Duck
        Game.Controls[pygame.K_SPACE] = Game.Fly

    def initEntities(self):
        print "DEBUG: Initializing Entities"
        EntityType.initializeEntityTypes()
        Game.Player = Entity(EntityType.EntityTypes['player'])
        Game.Player.flipped = False

    def initScreen(self):
        print "DEBUG: Initializing Screen"
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        Game.Screen = pygame.display.set_mode((Game.ScreenWidth, Game.ScreenHeight))

    def __init__(self):
        print "DEBUG: Initializing Game"
        pass
