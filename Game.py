
import logging
import math
import os

import pygame

from Entity import Entity
from Level import Level
from Object import Object
from ObjectType import ObjectType
from Player import Player
from Vector import Vector

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
    CollisionBlockSize = 1
    Gravity = -.5
    maxSlideSpeed = 1

    def _getCurrentObjectFrame(self, object):
        """
        Calculates the frame of the current animation for the given object to play.
        """
        object.currentFrame = object.currentAnimation.frame[(self.frameCount * object.currentAnimation.fps // Game.FPSLimit) % len(object.currentAnimation.frame)]
        if object.flipped:
            object.currentFrame = pygame.transform.flip(object.currentFrame, 1, 0)

        return object.currentFrame

    def _drawObject(self, object):
        """
        Draws the given object to the screen
        """
        if object.draw:
            Game.Screen.blit(self._getCurrentObjectFrame(object), (object.position.x, Game.ScreenHeight - (object.position.y + object.objectType.height)))

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
            entity.velocity.y += Game.Gravity

            #Velocity
            entity.velocity += entity.acceleration

            #Position
            entity.position += entity.velocity
            if (entity.position.y < 0):
                entity.position = Vector(20,Game.ScreenHeight)
                entity.velocity.y = 0

            entity.collideState = None

        #Collision
        for entity in Entity.Entities:
            #Reset collision values
            entity.collidingLeft,entity.collidingRight,entity.collidingTop,entity.collidingBottom = [False]*4

            for object in Object.Objects:
                entity.colliding(entity.detectCollision(object), object)

            if entity.projectile:
                if not entity.detectRectCollision(Game.currentLevel.rect):
                    entity.destroy = True

            if entity.destroy:
                Entity.Entities.remove(entity)
                continue

            if entity.collidingLeft or entity.collidingRight:
                entity.velocity.x = 0

            if entity.collidingTop or entity.collidingBottom:
                entity.velocity.y = 0

            if entity.wallSliding:
                if entity.velocity.y < -Game.maxSlideSpeed:
                    entity.velocity.y = -Game.maxSlideSpeed
        #Animation
        for entity in Entity.Entities:
            entity.getNextFrame()

    def _quit(self):
        """
        Quits the game (specifically when a user decides to)
        """

        logging.debug("User Quit")
        raise SystemExit("UserQuitException")

    def _handleEvents(self):
        """
        Handles all keyboard events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

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

        logging.info("Starting Game")
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
        except (KeyboardInterrupt, SystemExit):
            logging.debug("Exiting Game")
        finally:
            pygame.quit()

    def _initLevel(self):
        Game.currentLevel = Level('default')

        Game.Player = Player(ObjectType.ObjectTypes['player'], flipped = False)
        Object(ObjectType.ObjectTypes['block'], position = Vector(0, Game.ScreenHeight - (512 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(150, Game.ScreenHeight - (450 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(150, Game.ScreenHeight - (450 - 88 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(150, Game.ScreenHeight - (450 - 176 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(500, Game.ScreenHeight - (300 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(600, Game.ScreenHeight - (520 + ObjectType.ObjectTypes['block'].height)))
        Object(ObjectType.ObjectTypes['block'], position = Vector(660, Game.ScreenHeight - (300 + ObjectType.ObjectTypes['block'].height)))
        Game.Player.objectType.width -= 1
        Game.Player.objectType.height -= 2

    def _initControls(self):
        """
        Sets up the controls for MoveLeft,MoveRight,Jump,Duck,Fly,Quit
        """

        logging.debug("Initializing Controls")
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

        logging.debug("Initializing Entities")
        ObjectType.initializeObjectTypes()

    def _initScreen(self):
        """
        Sets up the pygame screen.
        """

        logging.debug("Initializing Screen")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        Game.Screen = pygame.display.set_mode((Game.ScreenWidth, Game.ScreenHeight))

    def __init__(self):
        """
        Initializes the game (doesn't do anything currently)
        """

        logging.debug("Initializing Game")
        self.frameCount = 0
        self._initScreen()
        self._initObjects()
        self._initControls()
        self._initLevel()
        self._start()
