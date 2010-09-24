import Entity
import EntityType
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
    Gravity = -4

    PlayerMaxJumpLength = 16
    PlayerMaxFlyLength = 16

    def drawFrame(self):
        Game.Screen.fill((0, 0, 0))
        i = 0
        while (i < Game.entityCount):
            Game.Screen.blit(Entity.Entities[i].getNextFrame(), Entity.Entities[i].position)
            i += 1

    def nextFrame(self):
        i = 0
        while i < Game.entityCount:
            Entity.Entities[i].x += Entity.Entities[i].vx
            Entity.Entities[i].y -= Entity.Entities[i].vy
            Entity.Entities[i].vy += Entity.Entities[i].ay
            if (Entity.Entities[i].falling):
                Entity.Entities[i].vy += Game.Gravity
            if (Entity.Entities[i].flying):
                Entity.Entities[i].fuel -= 2
            if (Entity.Entities[i].fuel <= 0):
                if (Entity.Entities[i].flying):
                    Entity.Entities[i].ay -= 6
                Entity.Entities[i].flying = False
            if (Entity.Entities[i].jumping):
                Entity.Entities[i].jumpcounter += 2
                if (Entity.Entities[i].jumpcounter > Game.PlayerMaxJumpLength):
                    Entity.Entities[i].jumping = False


            if (Entity.Entities[i].y + pygame.Surface.get_height(Entity.Entities[i].curFrame) > Game.wy):
                Entity.Entities[i].y = Game.wy - pygame.Surface.get_height(Entity.Entities[i].curFrame)
                Entity.Entities[i].vy = 0
                Entity.Entities[i].falling = False
                Entity.Entities[i].fuel = Game.PlayerMaxFlyLength
                Entity.Entities[i].ay = 0
                Entity.Entities[i].flying = False

    def registerInput(self, inputtype, press):
        Game.inputstate[inputtype] = press
        if (inputtype == Game.MoveLeft and press) or (inputtype == Game.MoveRight and not press):
            Game.Player.vx -= Game.PlayerHorizontalMoveSpeed
            if (inputtype == Game.MoveLeft) or (Game.Player.vx < 0):
                Game.Player.flipped = True
        elif (inputtype == Game.MoveLeft and not press) or (inputtype == Game.MoveRight and press):
            Game.Player.vx += Game.PlayerHorizontalMoveSpeed
            if (inputtype == Game.MoveRight) or (Game.Player.vx > 0):
                Game.Player.flipped = False
        elif (inputtype == Game.Jump and press and not Game.Player.falling):
            Game.Player.falling = True
            Game.Player.vy += 24
            Game.Player.jumping = True
        elif (inputtype == Game.Jump and not press):
            Game.Player.jumpcounter = 0
            Game.Player.jumping = False
            if (Game.Player.vy > 0 and not Game.Player.flying):
                Game.Player.vy = 0
        elif (inputtype == Game.Fly and press and not Game.Player.flying):
            Game.Player.flying = True
            Game.Player.ay += 6
            Game.Player.falling = True
        elif (inputtype == Game.Fly and not press and Game.Player.flying):
            Game.Player.ay -= 6
            Game.Player.flying = False

    def start(self):
        print "DEBUG: Starting Game"
#        nextFrameTime = 0
#        deltaFrameTime = 1000 / Game.FPSLimit
#        try:
#            while True:
#                # Event Polling
#                event = pygame.event.poll()
#                while event:
#                    if (event.type == pygame.QUIT or event.key == pygame.K_ESCAPE):
#                        print "User Quit"
#                        raise Exception("UserQuitException")
#
#                    elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
#                        #Register Keypresses:
#                        if Game.Controls.has_key(event.key):
#                            Game.registerInput(Game.Controls[event.key], event.type == pygame.KEYDOWN)
#
#                    event = pygame.event.poll()
#                currentTime = pygame.time.get_ticks()
#                if ((nextFrameTime - currentTime) <= 0):
#                    pygame.display.flip()
#
#                    Game.nextFrame()
#                    Game.drawFrame()
#                    nextFrameTime = currentTime + deltaFrameTime
#
#                pygame.time.delay(1)
#        except:
#            pygame.quit()

    def initControls(self):
        print "DEBUG: Initializing Controls"
        Game.Controls[pygame.K_a] = Game.MoveLeft
        Game.Controls[pygame.K_d] = Game.MoveRight
        Game.Controls[pygame.K_w] = Game.Jump
        Game.Controls[pygame.K_s] = Game.Duck
        Game.Controls[pygame.K_SPACE] = Game.Fly

    def initEntities(self):
        print "DEBUG: Initializing Entities"
        EntityType.EntityType.initializeEntityTypes()
        Game.Player = Entity.Entity((0, 0), EntityType.EntityType.EntityTypes['player'])
        Game.Player.flipped = False

    def initScreen(self):
        print "DEBUG: Initializing Screen"
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        Game.Screen = pygame.display.set_mode((Game.ScreenWidth, Game.ScreenHeight))

    def __init__(self):
        print "DEBUG: Initializing Game"
        pass
