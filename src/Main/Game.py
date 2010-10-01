from Player import Player
from Entity import Entity
from EntityType import EntityType
import pygame
import os

class Game:

    #Screen
    Screen = None
    ScreenWidth = 800
    ScreenHeight = 600
    FPSLimit = 60

    #Entities
    player = None

    #Controls
    Controls = {}
    ControlCount = 5
    ControlState = [False] * ControlCount
    MoveLeft, MoveRight, Jump, Duck, Fly = range(ControlCount)


    #Physics
    Gravity = .5

    def _drawFrame(self):
        """
        Draws the current frame to the screen
        """
        Game.Screen.fill((0, 0, 0))
        for entity in Entity.Entities:
            entity.currentFrame = entity.currentAnimation.frame[(self.frameCount * entity.currentAnimation.fps / Game.FPSLimit) % len(entity.currentAnimation.frame)]
            if entity.flipped:
                entity.currentFrame = pygame.transform.flip(entity.currentFrame, 1, 0)
            Game.Screen.blit(entity.currentFrame, entity.position)

    def _nextFrame(self):
        """
        Computes the current frame of the game
        """
        for entity in Entity.Entities:

            entity.position = [entity.position[i] + entity.velocity[i] for i in range(0, len(entity.position))]
            entity.velocity = [entity.velocity[i] + entity.acceleration[i] for i in range(0, len(entity.position))]
            if (entity.falling):
                entity.velocity[1] += Game.Gravity


            if (entity.position[1] + pygame.Surface.get_height(entity.currentFrame) > Game.ScreenHeight):

                entity.position[1] = Game.ScreenHeight - pygame.Surface.get_height(entity.currentFrame)
                entity.onLand()
            entity.getNextFrame()

    def _registerInput(self, inputType, press):
        """
        
        Registers the inputType key (press determines if it was pressed or released).
        Keys are:
            MoveLeft, MoveRight, Jump, Duck, Fly.
        
        """
        Game.ControlState[inputType] = press
        if (inputType == Game.MoveRight):
            Game.Player.run(press)
        elif (inputType == Game.MoveLeft):
            Game.Player.run(not press)
        elif (inputType == Game.Jump):
            Game.Player.jump(press)
        elif (inputType == Game.Fly):
            Game.Player.fly(press)

    def exit(self):
        """
        Exits the game with an exception
        """
        raise Exception("ExitException")

    def _quit(self):
        """
        Quits the game (specifically when a user decides to)        
        """
        print "User Quit"
        raise Exception("UserQuitException")

    def _handleEvents(self):
        event = pygame.event.poll()
        while event:
            if (event.type == pygame.QUIT):
                self._quit()

            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                #Register Keypresses:
                if (event.key == pygame.K_ESCAPE):
                    self._quit()
                if Game.Controls.has_key(event.key):
                    self._registerInput(Game.Controls[event.key], event.type == pygame.KEYDOWN)

            event = pygame.event.poll()


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

    def _initEntities(self):
        """
        Sets up the Entities and loads the EntityTypes into memory.  Also creates the player.
        """
        print "DEBUG: Initializing Entities"
        EntityType.initializeEntityTypes()
        Game.Player = Player(EntityType.EntityTypes['player'])
        Game.Player.flipped = False

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
        self._initEntities()
        self._initControls()
        self._start()
        print "DEBUG: Initializing Game"
        pass
