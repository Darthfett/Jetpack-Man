from Entity import Entity
from Level import Level
from Object import Object
from ObjectType import ObjectType
from Player import Player
import os
import pygame
import math

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

    #Levels
    currentLevel = None

    #Controls
    Controls = {}
    ControlCount = 7
    ControlState = [False] * ControlCount
    BoundControls = []
    MoveLeft, MoveRight, Jump, Duck, Fly, Fire, Quit = range(ControlCount)


    #Physics
    CollisionMap = []
    CollisionBlockSize = 1
    Gravity = .5
    maxSlideSpeed = 1
    
    def _getCurrentObjectFrame(self, object):
        """
        Calculates the frame of the current animation for the given object to play.
        """
        object.currentFrame = object.currentAnimation.frame[(self.frameCount * object.currentAnimation.fps / Game.FPSLimit) % len(object.currentAnimation.frame)]
        if object.flipped:
            object.currentFrame = pygame.transform.flip(object.currentFrame, 1, 0)
            
        return object.currentFrame

    def _drawObject(self, object):
        """
        Draws the given object to the screen
        """
        if object.draw:
            Game.Screen.blit(self._getCurrentObjectFrame(object), object.position)
            
    def _clearScreen(self):
        """
        Clears the screen
        """
        Game.Screen.fill((0, 0, 0))
        

    def _drawFrame(self):
        """
        Draws the current frame to the screen
        """

        self._clearScreen()
        
        for object in Object.Objects:
            self._drawObject(object)

        for entity in Entity.Entities:
            self._drawObject(entity)

        self._drawObject(Game.Player)


    def _handleInput(self):
        """
        
        Performs the Player's actions
        Actions are:
            MoveLeft, MoveRight, Jump, Duck, Fly, Fire.
        
        """

        Game.Player.running(Game.ControlState[Game.MoveRight], not (Game.ControlState[Game.MoveRight] == Game.ControlState[Game.MoveLeft]))
        Game.Player.jumping(Game.ControlState[Game.Jump])
        Game.Player.flying(Game.ControlState[Game.Fly])
        Game.Player.firing(Game.ControlState[Game.Fire])

    def _nextFrame(self):
        """
        Computes the current frame of the game
        """
        self._handleInput()        

        for entity in Entity.Entities:
        
            #Acceleration
            entity.velocity[1] += Game.Gravity

            #Velocity
            entity.velocity = [entity.velocity[i] + entity.acceleration[i] for i in range(len(entity.velocity))]

            #Position
            entity.position = [entity.position[i] + entity.velocity[i] for i in range(len(entity.position))]
            if (entity.position[1] > Game.ScreenHeight):
                entity.position = Game.currentLevel.start
                entity.velocity[1] = 0
            
            entity.collideState = None

        #Collision        
        for entity in Entity.Entities:
            #Reset collision values
            entity.collidingLeft,entity.collidingRight,entity.collidingTop,entity.collidingBottom = [False]*4
            
            for object in Object.Objects:
                entity.colliding(entity.detectCollision(object), object)
                
            if entity.destroy:
                Entity.Entities.remove(entity)
                continue
            
            if entity.collidingLeft or entity.collidingRight:
                entity.velocity[0] = 0
            
            if entity.collidingTop or entity.collidingBottom:
                entity.velocity[1] = 0
            
            if entity.wallSliding:
                if entity.velocity[1] > Game.maxSlideSpeed:
                    entity.velocity[1] = Game.maxSlideSpeed
        #Animation
        for entity in Entity.Entities:
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

        # Main Loop
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

    def _mapObject(self, object):
        """
        Maps the given object into the Collision Map
        """
        firstRow = object.position[0] / Game.CollisionBlockSize
        lastRow = int(math.ceil((object.position[0] + object.objectType.width) / Game.CollisionBlockSize))
        firstCol = object.position[1] / Game.CollisionBlockSize
        lastCol = int(math.ceil((abs(object.position[1]) + object.objectType.height) / Game.CollisionBlockSize))
        for row in range(firstRow, lastRow):
            for col in range(firstCol, lastCol):
                Game.CollisionMap[row][col].add(object)

    def _initLevel(self):
        Game.currentLevel = Level('default', ['objects.dat'])

        columnCount = int(math.ceil(Game.currentLevel.width / Game.CollisionBlockSize))
        rowCount = int(math.ceil(Game.currentLevel.height / Game.CollisionBlockSize))

        for row in range(rowCount):
            blocks = []
            for col in range(columnCount):
                blocks.append(set([]))
            Game.CollisionMap.append(blocks)

        Game.Player = Player(ObjectType.ObjectTypes['player'], flipped = False)
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (0, 512)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (150, 450)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (150, 450 - 88)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (150, 450 - 176)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (500, 300)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (600, 520)))
        self._mapObject(Object(ObjectType.ObjectTypes['block'], position = (660,300)))
        self._mapObject(Game.Player)
        Game.Player.objectType.width -= 1
        Game.Player.objectType.height -= 2

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
        Game.Controls[pygame.K_j] = Game.Fire
        Game.Controls[pygame.K_ESCAPE] = Game.Quit

        Game.BoundControls.append(pygame.K_a)
        Game.BoundControls.append(pygame.K_d)
        Game.BoundControls.append(pygame.K_w)
        Game.BoundControls.append(pygame.K_s)
        Game.BoundControls.append(pygame.K_j)
        Game.BoundControls.append(pygame.K_SPACE)
        Game.BoundControls.append(pygame.K_ESCAPE)

    def _initObjects(self):
        """
        Sets up the Objects and loads the Objects into memory.  Also creates the player.
        """

        print "DEBUG: Initializing Entities"
        ObjectType.initializeObjectTypes()
        Game.CollisionBlockSize = min(Game.ScreenHeight, Game.ScreenWidth)

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
        self._initLevel()
        self._start()
        print "DEBUG: Initializing Game"
        pass
