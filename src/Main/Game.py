from Object import Object
from Entity import Entity
from Player import Player
from ObjectType import ObjectType
import pygame
import os

class Game:

    #Screen
    Screen = None
    ScreenWidth = 800
    ScreenHeight = 600
    FPSLimit = 60

    #Objects
    Objects = []
    Entities = []
    Player = None

    #Controls
    Controls = {}
    ControlCount = 6
    ControlState = [False] * ControlCount
    BoundControls = []
    MoveLeft, MoveRight, Jump, Duck, Fly, Quit = range(ControlCount)


    #Physics
    Gravity = .5
    
    def _drawObject(self,object):
        """
        Draws the given object to the screen
        """
        
        object.currentFrame = object.currentAnimation.frame[(self.frameCount * object.currentAnimation.fps / Game.FPSLimit) % len(object.currentAnimation.frame)]
        if object.flipped:
            object.currentFrame = pygame.transform.flip(object.currentFrame, 1, 0)
        Game.Screen.blit(object.currentFrame, object.position)

    def _drawFrame(self):
        """
        Draws the current frame to the screen
        """
        
        Game.Screen.fill((0, 0, 0))
        for object in Object.Objects:
            self._drawObject(object)
            
        for entity in Entity.Entities:
            self._drawObject(entity)
            
        self._drawObject(Game.Player)
            

    def handleInput(self):
        """
        
        Performs the Player's actions
        Actions are:
            MoveLeft, MoveRight, Jump, Duck, Fly.
        
        """
        
        Game.Player.running(Game.ControlState[Game.MoveRight], not (Game.ControlState[Game.MoveRight] == Game.ControlState[Game.MoveLeft]))
        Game.Player.jumping(Game.ControlState[Game.Jump])
        Game.Player.flying(Game.ControlState[Game.Fly])
        
    

    def _nextFrame(self):
        """
        Computes the current frame of the game
        """
        
        self.handleInput()

        for entity in Entity.Entities:
            #Acceleration
            if (entity.isFalling):
                entity.velocity[1] += Game.Gravity
                pass

            #Velocity
            entity.velocity = [entity.velocity[i] + entity.acceleration[i] for i in range(len(entity.velocity))]

            #Position
            entity.position = [entity.position[i] + entity.velocity[i] for i in range(len(entity.position))]
            if (entity.position[1] + pygame.Surface.get_height(entity.currentFrame) > Game.ScreenHeight):
                entity.position[1] = Game.ScreenHeight - pygame.Surface.get_height(entity.currentFrame)
                entity.onLand()
            
            #Animation
            entity.getNextFrame()

    def _quit(self):
        """
        Quits the game (specifically when a user decides to)        
        """
        
        print "User Quit"
        raise Exception("UserQuitException")

    def _handleEvents(self):
        """        
        Handles all keyboard events        
        """
        
        pygame.event.pump()
        keyboardState = pygame.key.get_pressed()
        for key in Game.BoundControls:
            Game.ControlState[Game.Controls[key]] = keyboardState[key]
        if Game.ControlState[Game.Quit]:
            self._quit()

    def _start(self):
        """
        Starts the game
        Main loop
        Handles keyboard/mouse events        
        """
        
        print "DEBUG: Starting Game"
        nextFrameTime = 0
        deltaFrameTime = 1000 / Game.FPSLimit
        try:
            while True:
                self._handleEvents()

                currentTime = pygame.time.get_ticks()
                if ((nextFrameTime - currentTime) <= 0):
                    pygame.display.flip()
                    self.frameCount += 1
                    self._nextFrame()
                    self._drawFrame()
                    nextFrameTime = currentTime + deltaFrameTime

                pygame.time.delay(1)
        finally:
            pygame.quit()

    def _initControls(self):
        """
        Sets up the controls for MoveLeft,MoveRight,Jump,Duck,Fly,Quit
        """
        
        print "DEBUG: Initializing Controls"
        Game.Controls[pygame.K_a] = Game.MoveLeft
        Game.Controls[pygame.K_d] = Game.MoveRight
        Game.Controls[pygame.K_w] = Game.Jump
        Game.Controls[pygame.K_s] = Game.Duck
        Game.Controls[pygame.K_SPACE] = Game.Fly
        Game.Controls[pygame.K_ESCAPE] = Game.Quit

        Game.BoundControls.append(pygame.K_a)
        Game.BoundControls.append(pygame.K_d)
        Game.BoundControls.append(pygame.K_w)
        Game.BoundControls.append(pygame.K_s)
        Game.BoundControls.append(pygame.K_SPACE)
        Game.BoundControls.append(pygame.K_ESCAPE)

    def _initObjects(self):
        """
        Sets up the Objects and loads the Objects into memory.  Also creates the player.
        """
        
        print "DEBUG: Initializing Entities"
        ObjectType.initializeObjectTypes()
        Game.Player = Player(ObjectType.ObjectTypes['player'])
        Game.Player.flipped = False
        Object(ObjectType.ObjectTypes['block'], position=(150,450))
        Object(ObjectType.ObjectTypes['block'], position=(500,300))

    def _initScreen(self):
        """
        Sets up the pygame screen.
        """
        
        print "DEBUG: Initializing Screen"
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        Game.Screen = pygame.display.set_mode((Game.ScreenWidth, Game.ScreenHeight))

    def __init__(self):
        """
        Initializes the game (doesn't do anything currently)
        """
        
        self.frameCount = 0
        self._initScreen()
        self._initObjects()
        self._initControls()
        self._start()
        print "DEBUG: Initializing Game"
        pass
